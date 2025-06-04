# Windows Install Script

## Install

1. To use the script from [here](Windows/install.ps1):

```
# Save the script as install.ps1

# You might need to set execution policy first:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

This script will:

1. Check for Python installation
2. Install pip if not present
3. Create a virtual environment
4. Install required Python packages
5. Check and install AWS CLI if needed
6. Create an example CSV file
7. Provide instructions for next steps


After running the installation script, you'll need to:

1. Configure AWS credentials and create a profile (the profile will be used in the python file):

```
aws configure
```

1. Activate the virtual environment before running the main script
2. Update the Connect instance ID in the main script
3. Modify the example CSV file with your actual data

The scripts include error handling and provide feedback during the installation process. They also create an isolated virtual environment to avoid conflicts with other Python projects.
