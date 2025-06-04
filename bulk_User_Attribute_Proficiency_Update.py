import boto3
import csv
import time
from datetime import datetime
import logging
from typing import Optional, Tuple, List, Dict

class ConnectUserProfileManager:
    """
    Manages Amazon Connect user attributes using CSV input
    Supports username or user_id identification with attribute, value, and level
    """
    def __init__(self):
        """Initialize the AWS clients and set up logging"""
        #Use correct profile and change region to the region of your Connect instance
        session = boto3.Session(profile_name='<replace me>', region_name='<replace me>')
        self.connect = session.client('connect')
        self.instance_id = '<replace me>' #Change to your Connect instance id
        self.user_cache = {}  # Cache for username to user_id mappings
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'connect_attribute_updates_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_user_id_from_username(self, username: str) -> Optional[str]:
        """Look up user ID from username using Amazon Connect API"""
        if username in self.user_cache:
            return self.user_cache[username]

        try:
            paginator = self.connect.get_paginator('list_users')
            for page in paginator.paginate(
                InstanceId=self.instance_id,
                MaxResults=10
            ):
                for user in page['UserSummaryList']:
                    if (user.get('Username', '').lower() == username.lower() or 
                        user.get('IdentityInfo', {}).get('Email', '').lower() == username.lower()):
                        self.user_cache[username] = user['Id']
                        return user['Id']
            
            self.logger.error(f"No user found with username: {username}")
            return None

        except Exception as e:
            self.logger.error(f"Error looking up user ID for username {username}: {str(e)}")
            return None

    def read_csv_file(self, file_path: str) -> List[Dict]:
        """
        Read the CSV file containing user attribute updates
        
        Expected CSV format:
        identifier,identifier_type,action,attribute,value,level
        john.doe@example.com,username,add,Language,Spanish,5
        user123,user_id,remove,Language,French,0
        jane.smith,username,update,Skill,Sales,3
        """
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                return list(reader)
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {str(e)}")
            raise

    def get_current_attributes(self, user_id: str) -> Tuple[Optional[str], Optional[List]]:
        """Get current routing profile and attributes for a user"""
        try:
            response = self.connect.list_user_proficiencies(
                UserId=user_id,
                InstanceId=self.instance_id
            )
            # Initialize ProficiencyAttributes to empty list if it doesn't exist
            proficiency_attrs = response.get('UserProficiencyList', [])

            return proficiency_attrs
        except Exception as e:
            self.logger.error(f"Error getting attributes for user {user_id}: {str(e)}")
            return None, None

    def update_user_attributes(self, user_id: str, action: str, attributes: List) -> bool:
        if action == "add":
            # Updating the attributes for the user
            print(f"Adding Attributes: {attributes}")
            try:
                self.connect.associate_user_proficiencies(
                    InstanceId=self.instance_id,
                    UserId=user_id,
                    UserProficiencies=attributes
                )
                self.logger.info(f"Successfully updated attributes for user {user_id}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating attributes for user {user_id}: {str(e)}")
        elif action == "remove":
            # Removing the attributes for the user
            print(f"Removing Attributes: {attributes}")
            try:
                self.connect.disassociate_user_proficiencies(
                    InstanceId=self.instance_id,
                    UserId=user_id,
                    UserProficiencies=attributes
                )
                self.logger.info(f"Successfully updated attributes for user {user_id}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating attributes for user {user_id}: {str(e)}")

        else:
        # Update the attributes for the user
            print(f"Updating Attributes: {attributes}")
            try:
                self.connect.update_user_proficiencies(
                    InstanceId=self.instance_id,
                    UserId=user_id,
                    UserProficiencies=attributes
                )
                self.logger.info(f"Successfully updated attributes for user {user_id}")
                return True
            except Exception as e:
                self.logger.error(f"Error updating attributes for user {user_id}: {str(e)}")
        return False

    def are_attributes_equal(current_list, new_item_list):
        # Ensure new_item_list has exactly one item
        if len(new_item_list) != 1:
            return False
        
        new_item = new_item_list[0]
        
        # If current_list is empty, no match
        if not current_list:
            return False
            
        # Check if the new item matches any item in the current list
        for current_item in current_list:
            if (current_item['AttributeName'] == new_item['AttributeName'] and
                current_item['AttributeValue'] == new_item['AttributeValue'] and
                float(current_item['Level']) == float(new_item['Level'])):
                return True
                
        return False
    
    def process_updates(self, csv_file_path: str) -> Tuple[int, int]:
        """Process all updates from the CSV file"""
        updates = self.read_csv_file(csv_file_path)
        total = len(updates)
        successful = 0
        failed = 0
        skipped = 0

        for index, update in enumerate(updates, 1):
            try:
                identifier = update['identifier']
                identifier_type = update['identifier_type'].lower()
                action = update['action']
                attribute = update['attribute']
                value = update['value']
                level = update.get('level', '0')

                # Validate level
                if not level.isdigit() or not (0 <= int(level) <= 5):
                    self.logger.error(f"Invalid level {level} for {identifier} - must be 0-5")
                    failed += 1
                    continue

                # Get user_id based on identifier type
                user_id = (identifier if identifier_type == 'user_id' 
                          else self.get_user_id_from_username(identifier))

                if not user_id:
                    self.logger.error(f"Could not find user_id for identifier: {identifier}")
                    failed += 1
                    continue

                self.logger.info(
                    f"Processing {action} for {identifier_type} {identifier}: "
                    f"{attribute}.{value} = {level} ({index}/{total})"
                )

                # Get current user attributes
                current_attributes = self.get_current_attributes(user_id)

                # Assign new attributes to list                
                new_attributes = []
                new_attributes.append({
                    'AttributeName': attribute,
                    'AttributeValue': value,
                    'Level': int(level)
                })

                """
                #Uncomment to see attributes being processed in each call
                print("************")
                print(f"New Attributes: {new_attributes}")
                print(f"Current Attributes: {current_attributes}")
                print("************")
                """

                #Compares new attribute to existing
                attrs_exist = ConnectUserProfileManager.are_attributes_equal(current_attributes, new_attributes)
                if attrs_exist:
                    self.logger.warning(f"Attribute '{attribute}.{value} = {value}' already exists - skipping {action} for UserID: {user_id}")
                    skipped += 1
                    continue

                # Update the user
                if self.update_user_attributes(user_id, action, new_attributes):
                    successful += 1
                else:
                    failed += 1

                # Rate limiting - wait 1 second between requests
                time.sleep(0.5)

            except Exception as e:
                self.logger.error(f"Error processing update for row {index}: {str(e)}")
                failed += 1

        return successful, failed, skipped

def main():
    """Main execution function"""
    try:
        manager = ConnectUserProfileManager()
        
        csv_file_path = 'user_attribute_updates.csv'
        successful, failed, skipped = manager.process_updates(csv_file_path)
        
        manager.logger.info(f"""
        Processing complete:
        Successful updates: {successful}
        Failed updates: {failed}
        Skipped updates: {skipped}
        """)
        
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    main()