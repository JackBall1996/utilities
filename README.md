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

### Locally

The pre-commit package must be installed on your virtual environment and then activated using:

```bash
pre-commit install
```

The .pre-commit.config.yaml file specifies what hooks are to be run during each commit. As of right now, black and flake8 are currently run as part of our pre-commit checks.

### Repository

To ensure pre-commit checks are run on the github repository, a .github/workflows/pre_commit_checks.yml file must be created.

Once the file has been created in the correct folder and pushed to the repo, it should automatically run under the conditions specified.

## Git Cheat Sheet ##

| Command                         | Action                              | 
| ------------------------------- | ----------------------------------- |
| $ git clear                     | Clear terminal                      |
| $ git clone [url] [folder_name] | Clone a repo (optional folder name) |
| $ git add [file_name]           | Add a file                          |
| $ git rm [file_name]            | Remove a file                       |
| $ git branch                    | List all branches                   |
| $ git branch [branch_name]      | Create a new branch                 |
| $ git branch -d [branch_name]   | Delete a merged branch              |
| $ git branch -D [branch_name]   | Delete any kind of branch           |
| $ git switch [branch_name]      | Switch to a branch                  |
| $ git diff                      | List differences between branch and repo |
| $ git diff [file_path] | List differences in a specific file | 
| $ git diff > [file_path].diff | Save differences to specified file path | 
| $ git remote update | Update connection (allows new branches to appear) | 
| $ git log | List commit history on active branch | 
| $ git pull origin [branch_name] | Update local repo | 
| $ git commit -m [message] | Commit changes | 
| $ git push | Push commits to repo | 
| $ git stash | Temporarily shelve any changes | 
| $ git stash pop [index] | Reapply shelved changes (Index defaults to 0) | 
| $ git stash list | List all stashes |
| $ git stash show [index] | Show all changes for specific stash | 
## To-Do

- Add MKDocs
- Add pyproject.toml
- Add pull request template
