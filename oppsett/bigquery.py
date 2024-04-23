import os
from google.cloud import bigquery

def init_bigquery_client():
    credentials_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')

    authenticated_locally = os.path.isfile(credentials_path)
    running_in_prod = os.getenv('NAIS_CLUSTER_NAME', '').lower() == 'prod-gcp'

    if authenticated_locally or running_in_prod:  # Check if the file exists
        if authenticated_locally:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

        return bigquery.Client(project='flex-prod-af40')
    else:
        print("Credentials file not found OR not running in prod. Functionality requiring credentials/prod env will "
              "be skipped.")
