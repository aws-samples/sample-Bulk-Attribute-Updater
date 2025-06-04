echo "Installing Connect User Profile Manager dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
echo "Python 3 is not installed. Please install Python 3 first."
exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
echo "pip3 is not installed. Installing pip..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
rm get-pip.py
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install —upgrade pip
pip install boto3
pip install typing

# Check AWS CLI installation
if ! command -v aws &> /dev/null; then
echo "AWS CLI is not installed. Installing AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
fi

echo "Creating example CSV file..."
cat > user_attribute_updates.csv << EOL
identifier,identifier_type,action,attribute,value,level
[john.doe@example.com](mailto:john.doe@example.com),username,add,Language,Spanish,5
EOL

echo "Installation complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "Please ensure you have configured your AWS credentials using 'aws configure'"
