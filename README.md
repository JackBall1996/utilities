# Utilities

## Virtual Environments

### Creation

- Open command promot
- Set your working directory using:
    ```bash
    cd C:\your_working_directory\
    ```
- To create a virtual environment named 'env' run:
    ```bash
    py -m venv env
    ```

### Activation / De-activation

- Activate
    ```bash
    env\scripts\activate
    ```
- Deactivate'deactivate'
    ```bash
    deactivate
    ```

### Packages

You can now install packages in your virtual environment using the following command:

```bash
py -m pip install some_package
```

Within your environment you can generate a list of all the packages that are currently installed and required for the project by running the following command:

```bash
pip freeze > requirements.text
```

You can install all the packages and their versions from a requirements file by using the following command:

```bash
pip install -r requirements.text
```

### Extras 

- You can use the command 'where python' in command prompt to check python is running from your virtual environment
- VS Code, press control + shift + p and search 'interpreter' to choose your default python interpreter. You can select your virtual environment from here.

## Dagster

### Set-Up

- Open command prompt 
- Set working directory to Dagster folder
- Activate your virtual environment
- Launch Dagster 
    ```bash
    dagster dev -f my_python_script.py
    ```
- Open Dagster UI http://127.0.0.1:3000/locations/

## Pre-Commit

The pre-commit package must be installed on your virtual environment and then activated using:

```bash
pre-commit install
```

The .pre-commit.config.yaml file specifies what hooks are to be run during each commit. As of right now, black and flake8 are currently run as part of our pre-commit checks.

## To-Do

- Add MKDocs
- Add pyproject.toml