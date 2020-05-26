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

To create the Cloud Function, follow the steps below:-

- Go to **Cloud Functions** in the left navigation bar
- Click **Create Function**
- Name the function, e.g. **Dome9-Onboarder**
- Set **Memory Allocated** to **128MB**
- Leave **Trigger** as the default **HTTP**
- In the **Source Code** section, either copy and paste the text from the **main.py** file in the repo or upload the **function.zip** file from the repo, same for **requirements.txt**. If using the **ZIP Upload** method, select a **staging bucket** for the upload
- Set the **Runtime** to be **Python 3.7**
- Set **Function to execute** to **add_project**
- Click **Environment variables, Networking, Timeouts and More**
- In the **Environment** section, click **Add Variable** and add environment variables for the following:-
    - D9_API_KEY
    - D9_API_SECRET
    - GCP_SM_PROJECT_ID - *Security project ID where Secret Manager deployed, e.g. my-security-project-999999*
    - GCP_SECRET_ID - *Name of secret*
    - GCP_SECRET_VERSION - *Version number of secret (e.g. 1)*
- Click **Create**, this will take a few minutes to deploy and shows green when successful in the console
- Once deployed, the function can be tested by clicking the **Triggers** tab and clicking the trigger URL. The browser response should simply read **OK**. If it does not, check the Service Account IAM permissions.

**Creating the Cloud Scheduler Job**

In order to run the onboarder script on a schedule, we need to create a job in **Cloud Scheduler**, which is basically "cron in the cloud". Perform the steps below:-

- Create a new Service Account for Cloud Scheduler in the security project
    - Set the **Name** as *SA-Cloud-Scheduler* (or whatever makes sense). **Note the account e-mail address, you will need this later**
    - Set the **Description** to be *Service Account for HTTP Scheduler* (or whatever)
    - Click **Create**
    - Add the **Project Owner** role to the Service Account 
    - Click **Done**
   
- Create a new Cloud Scheduler job by following the steps below:-
    - Go to **Tools | Cloud Scheduler** in the left navigation bar
    - Click **Create Job**
    - Set the Job Name *D9-Onboarder* (or whatever)
    - Set the optional job **Description**
    - Set the job **Frequency** in standard Cron format *(e.g. 0 6 * * * will set the job to run at 0600 daily)*
    - Set the appropriate **Time Zone**
    - In **Target** settings, set **HTTP**
    - In the **URL** field, add the URL of the **Cloud Function** you defined earlier
    - Leave the **HTTP Method** at the default of **POST**
    - Click **Show More**
    - Under **Auth header**, select **Add OIDC token**
    - Under **Service Account**, paste the e-mail address of the **Service Account** created in the step above (SA-Cloud-Scheduler)
    - Under **Audience**, paste in the **URL of the Cloud Function**
    - Click **Create**
    
The job will take a few seconds to create. Once complete, you can test it manually by clicking **Run Now** and viewing the logs.

    

    
