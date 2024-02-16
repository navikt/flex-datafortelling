# %% [markdown]
# # Hello World in a Jupyter-compatible Python Script

# %% [code]
print("Hello, World!")

# %% [markdown]
# This is another markdown cell.
# %% [code]
# the above determines wether code is shown or not
import matplotlib.pyplot as plt

# Data for plotting
x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]

# Create the plot
plt.plot(x, y)

# Add title and labels
plt.title('Hello World Graph')
plt.xlabel('x-axis')
plt.ylabel('y-axis')

# Show the plot
plt.show()
# %% [code]
from datetime import datetime

import os
from google.cloud import bigquery

credentials_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')

authenticated_locally = os.path.isfile(credentials_path)
running_in_dev = os.getenv('ENVIRONMENT', '').lower() == 'dev'
running_in_prod = os.getenv('ENVIRONMENT', '').lower() == 'prod'

if authenticated_locally or running_in_prod:  # Check if the file exists
    if authenticated_locally:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    bigquery_client = bigquery.Client(project='flex-prod-af40')

    query = """


    SELECT *
    FROM `flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`
    limit 100
    """

    query_job = bigquery_client.query(query)
    df = query_job.to_dataframe()

    print(f'dataframe length: {len(df)}')

    df.head()
else:

    print(
        "Credentials file not found OR not running in prod. Functionality requiring credentials/prod env will be skipped.")

# %% [code]
print(datetime.now())
# %% [markdown]
# hello world





