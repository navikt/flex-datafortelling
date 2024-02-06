# %% [markdown]
# # Hello World in a Jupyter-compatible Python Script

# %% [code]
print("Hello, World!")

# %% [markdown]
# This is another markdown cell.
# %% [code]
#| echo: true
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
#| echo: false
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='/Users/kuls/.config/gcloud/application_default_credentials.json'
import json
from google.cloud import bigquery

bigquery_client = bigquery.Client(project='flex-dev-2b16')

"""
   SELECT *
FROM `flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`
WHERE sporsmal_tag = "FRAVAR_FOR_SYKMELDINGEN_NAR"
  AND DATE(sendt) >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
"""

query = """


SELECT *
FROM `flex-prod-af40.flex_dataset.sykepengesoknad_sporsmal_svar_view`
limit 10
"""


query_job = bigquery_client.query(query)
df = query_job.to_dataframe()

df.head()
# Specify the file path for the JSON file
# file_path = 'data_v1.json'

# Write the DataFrame to a JSON file
# df.to_json(file_path, orient='records', lines=True) # I want it as a list, more parseable
#  df.to_json(file_path, orient='records')


# %% [code]
import json
# %% [markdown]
# hello world