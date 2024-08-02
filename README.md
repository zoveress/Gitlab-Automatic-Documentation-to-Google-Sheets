**Prerequisites:**

Define the following environment variables before you run the script:

**$GITLAB_TOKEN** - Personal Access API token for your gitlab.com account. [Follow this link](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) to see how get one.

**$GOOGLE_SHEET_CREDENTIALS_FILE** - Path to the json formatted file containing your google credentials. [Follow this link](https://developers.google.com/workspace/guides/create-credentials) to see how to get one.

**$SHEET_NAME** - Name of the google sheet you would like to use for the documentation. It has to be created manually before the script runs.

**$SLEEP** - The time in seconds the procedure should sleep before runs again. 

I have also included a docker file with dummy variables in case you would like to run it on Docker or Kubernetes.

**Usage:**

python3 gitlab.py
