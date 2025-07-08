# Utilities

## Virtual Environments

### Creation

- Open command promot
- Set your working directory using 'cd C:\your_working_directory\'
- Run 'py -m venv env' to create a virtual environment named 'venv' 

### Activation / De-activation

- Run 'venv\scripts\activate'
- Run 'deactivate'

### Packages

You can now install packages in your virtual environment using the following command:

- py -m pip install some_package

Within your environment you can generate a list of all the packages that are currently installed and required for the project by running the following command:

- pip freeze > requirements.text

You can install all the packages and their versions from a requirements file by using the following command:

- pip install -r requirements.text

### Extras 

- You can use the command 'where python' in command prompt to check python is running from your virtual environment
- VS Code, press control + shift + p and search 'interpreter' to choose your default python interpreter. You can select your virtual environment from here.

## Dagster

### Set-Up

- Open command prompt 
- Set working directory to Dagster folder using 'cd C:\my_folder_path\
- Activate your virtual environment '.pyenv\scripts\activate'
- Launch Dagster 'dev -f my_python_script.py'
- Open Dagster UI http://127.0.0.1:3000/locations/

## To-Do

- Add pre-commit
- Add MKDocs