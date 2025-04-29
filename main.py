import os
import json
import ndjson
import requests
import google.oauth2.id_token
import google.auth.transport.requests
from google.cloud import storage
import pandas as pd

def main():
    storeDataToBucket()

def getRawData():
    '''
        Calls google cloud and gets the raw data.
    '''
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
    return r.text
    # response_dict = r.json()
    
    # # Pretty Printing JSON string back 
    # return json.dumps(response_dict, indent=4, sort_keys=True)

def storeDataToBucket():
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    bucket_name = "dog-breed-data"

    # The ID of your new GCS object
    blob_name = "dog-breed-data-raw-new-test"

    # The data to store in the bucket
    data = getRawData()

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        f.write(data)

def read_from_bucket():
    """Write and read a blob from GCS using file-like IO"""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../pynes-case-50f5db6cfad9.json'
    request = google.auth.transport.requests.Request()
    audience = 'https://rawdataget-978661416923.us-central1.run.app/read_from_bucket'
    TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)

    r = requests.post(
        audience, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"}
        )

    # Convert json into dictionary 
    response_dict = r.json()
    
    # Pretty Printing JSON string back 
    return json.dumps(response_dict, indent=4, sort_keys=True)

def delete_blob(blob_name):
    """Deletes a blob from the bucket."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../pynes-case-50f5db6cfad9.json'
    request = google.auth.transport.requests.Request()
    audience = 'https://rawdataget-978661416923.us-central1.run.app/delete_blob'
    TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)

    r = requests.delete(
        audience, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"}
        )

    # return status and reason
    return r.status_code, r.reason

def write_to_table():
    """Deletes a blob from the bucket."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../pynes-case-50f5db6cfad9.json'
    request = google.auth.transport.requests.Request()
    audience = 'https://rawdataget-978661416923.us-central1.run.app/write_to_table'
    TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)

    r = requests.post(
        audience, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"}
        )

    # return status and reason
    return r.status_code, r.reason



if __name__ == "__main__":
    storeDataToBucket()
    