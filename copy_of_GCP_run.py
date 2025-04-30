import functions_framework
import requests
import ndjson
import datetime
from google.cloud import storage
from google.cloud.bigquery_datatransfer_v1 import (
    DataTransferServiceClient,
    StartManualTransferRunsRequest,
)

@functions_framework.http
def main(request):
    """
    Main function that GET the data from the api, stores it in a bucket and runs transfer job to store in table.
    """
    store_data_to_bucket()
    write_to_table()

@functions_framework.http
def rawDogBreedDataGet(request):
    """HTTP Cloud Function.
    Returns:
        Raw data from the dog breed api
    """
    r = requests.get("https://api.thedogapi.com/v1/breeds")
    # Format to new line delimited json.
    formatted_data = ndjson.dumps(r.json())
    return formatted_data

@functions_framework.http
def store_data_to_bucket():
    """Write a blob from GCS"""
    # The ID of your GCS bucket
    bucket_name = "dog-breed-data"

    # The ID of your new GCS object
    blob_name = "dog-breed-data-raw-1"

    # The data to store in the bucket
    r = requests.get("https://api.thedogapi.com/v1/breeds")
    # Format to new line delimited json.
    data = ndjson.dumps(r.json())

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        f.write(data)
    return blob

@functions_framework.http
def read_from_bucket():
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    bucket_name = "dog-breed-data"

    # The ID of your new GCS object
    blob_name = "dog-breed-data-raw"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("r") as f:
        return f.read()

@functions_framework.http
def write_to_table():
    # Create a client object
    client = DataTransferServiceClient()

    # Transfer configuration name
    transfer_config_name = "projects/978661416923/locations/us/transferConfigs/683339e6-0000-2cc2-aa57-94eb2c0b2418/runs/6815085f-0000-26ee-81b2-883d24f35048"
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(days=5)
    end_time = now - datetime.timedelta(days=2)

    # Some data sources, such as scheduled_query only support daily run.
    # Truncate start_time and end_time to midnight time (00:00AM UTC).
    start_time = datetime.datetime(
        start_time.year, start_time.month, start_time.day, tzinfo=datetime.timezone.utc
    )
    end_time = datetime.datetime(
        end_time.year, end_time.month, end_time.day, tzinfo=datetime.timezone.utc
    )

    requested_time_range = StartManualTransferRunsRequest.TimeRange(
        start_time=start_time,
        end_time=end_time,
    )

    # Initialize request argument(s)
    request = StartManualTransferRunsRequest(
        parent=transfer_config_name,
        requested_time_range=requested_time_range,
    )

    # Make the request
    response = client.start_manual_transfer_runs(request=request)

    # Handle the response
    print("Started manual transfer runs:")
    for run in response.runs:
        print(f"backfill: {run.run_time} run: {run.name}")
    return response
    