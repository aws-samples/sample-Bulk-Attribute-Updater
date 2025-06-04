# Install script for Windows
Write-Host "Installing Connect User Profile Manager dependencies..."

# Check if Python is installed
try {
    python --version
}
catch {
    Write-Host "Python is not installed. Please install Python 3 first."
    Write-Host "Visit: https://www.python.org/downloads/"
    exit 1
}

# Check if pip is installed
try {
    pip --version
}
catch {
    Write-Host "pip is not installed. Installing pip..."
    Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
    python get-pip.py
    Remove-Item get-pip.py
}

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install required packages
Write-Host "Installing required packages..."
pip install --upgrade pip
pip install boto3
pip install typing

# Check AWS CLI installation
try {
    aws --version
}
catch {
    Write-Host "AWS CLI is not installed. Installing AWS CLI..."
    Invoke-WebRequest -Uri https://awscli.amazonaws.com/AWSCLIV2.msi -OutFile AWSCLIV2.msi
    Start-Process msiexec.exe -Wait -ArgumentList '/i AWSCLIV2.msi /quiet'
    Remove-Item AWSCLIV2.msi
}

# Create example CSV file
Write-Host "Creating example CSV file..."
@"
identifier,identifier_type,action,attribute,value,level
john.doe@example.com,username,add,Language,Spanish,5
"@ | Out-File -FilePath "user_attribute_updates.csv" -Encoding UTF8

Write-Host "Installation complete!"
Write-Host "To activate the virtual environment, run: .\venv\Scripts\Activate.ps1"
Write-Host "Please ensure you have configured your AWS credentials using 'aws configure'"
