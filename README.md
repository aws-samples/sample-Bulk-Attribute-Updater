# Connect User Profile Manager

A Python utility for managing Amazon Connect user attributes through CSV-based bulk updates.

## Overview

This tool allows you to bulk update user attributes and proficiency levels in Amazon Connect using a CSV file. It supports adding, removing, and updating attributes for users identified by either their username or user ID.

## Prerequisites

* Python 3.x
* AWS credentials configured with appropriate permissions
* boto3 library installed
* Access to Amazon Connect instance

  **If Pyhton is not installed, run the install script for your OS in this repo to setup your environment.

## Installation

1. Install required dependencies:

```
pip install boto3
```

2. Configure AWS credentials using AWS CLI or credentials file with a named profile

***Ensure your credentials have the correct permissions*

3. Update the bulk_User_Attribute_Proficiency_Update.py with correct values for your environment.
    * line 16 profile_name and region_name
    * line 18 instance_id (use the GUID)

4. Create the csv file using the format shown in the next section.

5. Run the script and monitor output

# CSV File Format

Sample csv found [here](user_attribute_updates_template.csv)

## Create a CSV file named 

```
user_attribute_updates.csv
```

 with the following columns:

```
identifier,identifier_type,action,attribute,value,level
```

### Column Descriptions:

```
identifier
```

: Username or user ID (depending on identifier_type)

```
identifier_type
```

: Either 'username' or 'user_id'

```
action
```

: Must be one of: 'add', 'remove', or 'update'

```
attribute
```

: The attribute name to modify

```
value
```

: The attribute value

```
level
```

: Proficiency level (0-5)

# Python Script Usage

1. Update the profile_name, region_name and instance_id in the python code with your Amazon Connect instance ID


1. Prepare your CSV file with the required updates
2. Run the script:

```
python bulk_User_Attribute_Proficiency_Update.py
```

## Features

* Supports bulk updates through CSV
* Caches user lookups for better performance
* Comprehensive logging
* Rate limiting to prevent API throttling
* Validation of input data
* Skips duplicate attribute updates
* Handles three types of operations: add, remove, update

## Logging

The script creates a log file with the format:connect_attribute_updates_YYYYMMDD_HHMMSS.log

## Error Handling

The script handles various error scenarios:

* Invalid CSV format
* User not found
* Invalid proficiency levels
* API errors
* Missing or incorrect data

## Output

After processing, the script provides a summary of:

* Successful updates
* Failed updates
* Skipped updates (duplicates)

## Best Practices

* Always test with a small batch of users first
* Back up existing user configurations before making bulk changes
* Review logs after execution to verify changes
* Maintain proper AWS permissions
* Keep CSV file properly formatted

## Limitations

* Proficiency levels must be between 0 and 5
* Rate limited to 1 request per second
* Requires appropriate AWS permissions
* Username lookups are case-insensitive

## Troubleshooting

If you encounter issues:

* Check the log file for specific error messages
* Verify AWS credentials and permissions
* Ensure CSV format is correct
* Verify Connect instance ID is correct
* Check network connectivity





