# Dog-Breed-Explorer
This project uses BigQuery and dbt to explore the data from [thedogapi](https://api.thedogapi.com/v1/breeds)

## In order to bootstrap this repo.
  ### 1. Clone repo
  ### 2. Install requirements from pyproject.toml
    run poetry install
  ### 3. Create the following git secrets
    DBTCLOUDAPIKEY # user token
    DBT_PROFILES_YML # Profile.yml
    DBT_SERVICE_ACCOUNT # Serviceaccount.yml
  ### 4. Create GCP service account
    Change GOOGLE_APPLICATION_CREDENTIALS in main to point to the credentials json fild    


