import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../pynes-case-50f5db6cfad9.json'
request = google.auth.transport.requests.Request()
audience = 'https://rawdataget-978661416923.us-central1.run.app/rawDogBreedDataGet'
TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)

r = requests.post(
    audience, 
    headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
    json=json.dumps({"key": "value"})  # possible request parameters
)

# Convert json into dictionary 
response_dict = r.json()
  
# Pretty Printing JSON string back 
print(json.dumps(response_dict, indent=4, sort_keys=True))


# print(requests.get("https://api.thedogapi.com/v1/breeds").text)
# r1 = requests.get("https://api.thedogapi.com/v1/breeds")
# print(r1.status_code, r1)