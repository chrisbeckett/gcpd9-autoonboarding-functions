What does this script do?
-------------------------

This is a python script which automates onboarding of GCP projects linked to a G-Suite Organisation, using Google Functions. It uses a combination of GCP services to run on a schedule and pull secrets from GCP Secret Manager.

Pre-requisites
--------------
To run this script, you will need the following:-

1) **Python 3.6** (or newer)

2) A **GCP Project** into which the Secret Manager and Function will be deployed

3) A **GCP Secret Manager** instance in the security project

4) A functions **Service Account** with appropriate permissions and it's corresponding **JSON** key file stored locally

5) A **Cloud Scheduler Service Account** to trigger the function on a cron schedule in a secure manner

6) Run **git clone https://github.com/chrisbeckett/gcpd9-autoonboarding-functions.git**

6) Run **python -m venv gcpd9-autoonboarding-functions**

7) Run **scripts\activate.bat** to enable the Python virtual environment

8) Run **pip install -r requirements.txt** to install required Python modules
    
Setup
-----

**Service Account**

The first step is to create an **IAM Service Account** to use for the Secret Manager retrieval. Go to the project in which the Secret Manager and function are to be deployed and follow the steps below:-

- Click **IAM** and then **Service Accounts** from the left navigation bar
- Click **Create service account**
    - Give the service account a meaningful name, such as **Dome9-Onboarder**
    - Check the service account ID is automatically filled. **Copy this address somewhere handy as you will need it later**
    - Give the service account a description, such as **"Dome9 Onboarder SA**
    - Click **Create**
- In **Service Account Permissions**, add the **Secret Manager Secret Accessor** role to the account
- **Add another role** and add the role **Cloud Functions Admin**
- Click **continue**
- Click **Keys** and **Create Key**
- Leave the default key format as **JSON** and click **Create**
- Note the downloaded key file location, you will need this later
- Click **Done** and verify the Service Account has the correct permissions for the project

**Secret Manager**

Prior to deploying the function, you need to add the GCP credentials into **Secret Manager**. **Enable the Secret Manager API** (if not already enabled) and perform the following steps:-

- Go to **Security** and **Secret Manager** in the left navigation bar
- Click **Create Secret**
- Give the secret a meaningful name (Dome9-onboarder, for example)
- Upload the **JSON secret file** you downloaded from earlier when creating the GCP Service Account
- Select the region to store the secret (optional)
- Click **Create Secret**, this should create a **Version 1** of your secret, status **Enabled**

**Creating the Function**

To run the script locally, you need to set several environment variables which are then read in by the script. This prevents any secret keys being hard coded into the script. Set the following:-

- SET AZURE_TENANT_ID=xxxxxxxxxx
- SET AZURE_CLIENT_ID=xxxxxxxxxxx
- SET AZURE_CLIENT_SECRET=xxxxxxxxxxxxxxx

Running the script
------------------
Simply run the script **d9-sizer.py** from the command line 

Disclaimer
==========
This tool is to be used to provide indicative numbers of billable assets in an Azure environment for cost analysis purposes. No warranty implied.




