# Dog-Breed-Explorer
This project primarely uses BigQuery and dbt to explore the data from [thedogapi](https://api.thedogapi.com/v1/breeds)

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
  ### 5. Run main.py

## Findings & business impact
Finding the perfect dog for you is a challenge. Dogs come in many shapes and sizes has just about as many different temperaments as us humans. The good news is the findings of this project can help narrow the search. First and foremost, we have concluded that there is a clear correlation between the height and weight of the average dog. Secondly, we have concluded that the dogs within the Terrier & Toy breed groups live the longest, while Hounds, Working & Mixed dogs have the shortest expected lifespan. The breed group Mixed does however have the lowest variance of the expected life span. Comparing life span with weight of the breeds shows that smaller dogs are expected to live longer than larger dogs, which ties in perfectly with the breed groups Terrier & Toy living the longest and Hound & Working breed groups living the shortest. Furthermore, the Mixed breed group having the lowest variance in expected life span makes perfect sense as these dogs are a mix of other breeds and therefore across enough observations tends towards a general mean. Finally, we can conclude that if a dog is categorized as a family dog it usually also has traits such as "intelligent", "Alert" & "Loyal", and in general exhibits "likeable" temperaments.

Utilizing these findings, we can help new dog owners by narrowing the search for their perfect dog. Whether it being a large protective dog they are looking for, or a smaller couch dog. 


