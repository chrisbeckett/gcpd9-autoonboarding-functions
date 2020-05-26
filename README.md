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




