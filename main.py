from google.cloud import resource_manager
from google.cloud import secretmanager
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

added_accounts = 0

def add_project(req):
    try:
        # Create the Secret Manager and Resource Manager client.
        client = secretmanager.SecretManagerServiceClient()
        gcp_client = resource_manager.Client()
        # Read in required environment variables
        d9_api_key = os.environ['D9_API_KEY']
        d9_api_secret = os.environ['D9_API_SECRET']
        gcp_sm_project_id = os.environ['GCP_SM_PROJECT_ID']
        gcp_secret_id = os.environ['GCP_SECRET_ID']
        gcp_secret_version = os.environ['GCP_SECRET_VERSION']
        # Access the secret version
        secret_path = client.secret_version_path(gcp_sm_project_id, gcp_secret_id, gcp_secret_version)
        print("Secret path is: ",secret_path)
        response = client.access_secret_version(secret_path)
        print("Response :", response)
        secret_payload = response.payload.data.decode('UTF-8')
        print("Payload is: ",secret_payload)
        data = json.loads(secret_payload)
        print("Data is: ", data)
        # Set header parameters for Dome9 HTTP POST
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # Verify the environment variables have been set
        if 'D9_API_KEY' in os.environ:
            pass
        else:
            print("ERROR : The Dome9 API key has not been defined in environment variables")
            sys.exit(0)
        if 'D9_API_SECRET' in os.environ:
            pass
        else:
            print("ERROR : The Dome9 API key secret not been defined in environment variables")
            sys.exit(0)
        if 'GCP_SM_PROJECT_ID' in os.environ:
            pass
        else:
            print("ERROR : The Google Cloud GCP Secret Manager project location has not been defined in environment variables")
            sys.exit(0)
        if 'GCP_SECRET_ID' in os.environ:
            pass
        else:
            print("ERROR : The ID of the Secret in Google Cloud Secret Manager has not been defined in environment variables")
            sys.exit(0)
        if 'GCP_SECRET_VERSION' in os.environ:
            pass
        else:
            print("ERROR : The version of the Secret in Google Cloud Secret Manager has not been defined in environment variables")
            sys.exit(0)        
        added_accounts = 0
        print("===================================================================================================================")
        print("                                             Dome9 GCP Onboarding Tool")
        print("===================================================================================================================","\n")
        for project in gcp_client.list_projects():
            print("Projects found: ",project.project_id)
            print("In the loop")
            data.update({'project_id': project.project_id})
            newval = data.get("project_id")
            print("===================================================================================================================")
            print("Project ID updated to: ",newval)
            print("Project found:", project.name, "Project ID: ",project.project_id)
            payload = {'name': project.name,'serviceAccountCredentials': data}
            r = requests.post('https://api.dome9.com/v2/GoogleCloudAccount',json=payload, headers=headers, auth=(d9_api_key, d9_api_secret))
            if r.status_code == 201:
                print('Project successfully added to Dome9:', project.name)
                print("===================================================================================================================","\n")
                added_accounts = added_accounts + 1
            elif r.status_code == 400:
                print('There was an error with the project, please check credentials and that it does not already exist in Dome9',"\n")
            elif r.status_code == 401:
                print('Bad credentials onboarding project to Dome9:',project.name,"\n")
            elif r.status_code == 500:
                print('Error onboarding project to Dome9, check dependent APIs are enabled in GCP:',project.name,"\n")
            else:
                print('Unknown error onboarding subscription to Dome9:',project.name,'Status Code:', r.status_code)
                print(r.content,"\n")
    except:
        print("Unknown error, sorry!")

print("\n")
print("===================================================================================================================")
print("                                           RUN COMPLETE - SUMMARY RESULTS")
print("===================================================================================================================","\n")
print("Number of GCP projects successfully added to Dome9: ", added_accounts)
print("===================================================================================================================","\n")
