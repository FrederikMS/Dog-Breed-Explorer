import os
import json
import ndjson
import requests
import google.oauth2.id_token
import google.auth.transport.requests
from google.cloud import storage, bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../pynes-case-50f5db6cfad9.json"
bucket_name = "dog_test_new_bucket"
destination_blob_name = "dog_test_new_blob"
project_id = "pynes-case"
table_name = "dog_test_new_table"
dataset_name = "dog_test_new_dataset"


def create_gcp_bucket():
    """Creates a new bucket."""

    storage_client = storage.Client()

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
    # Enable versioning
    bucket.versioning_enabled = True
    bucket.patch()


def create_bucket_object():
    """
    Fetches JSON from an API and uploads it to a GCS bucket.
    """
    # Fetch JSON from API
    response = requests.get("https://api.thedogapi.com/v1/breeds")
    response.raise_for_status()  # Raise an error for bad status codes

    new_line_delimited_json = ndjson.dumps(response.json())

    # Initialize GCS client and get bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload from bytes
    blob.upload_from_string(new_line_delimited_json, content_type="application/json")

def create_bigquery_dataset():
    client = bigquery.Client(project=project_id)
    dataset_ref = bigquery.Dataset(f"{project_id}.{dataset_name}")
    dataset_ref.location = "us"
    dataset = client.create_dataset(dataset_ref, exists_ok=True)

def create_bigquery_table():
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_name).table(table_name)

    schema = schema = [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("bred_for", "STRING"),
        bigquery.SchemaField("breed_group", "STRING"),
        bigquery.SchemaField("life_span", "STRING"),
        bigquery.SchemaField("origin", "STRING"),
        bigquery.SchemaField("temperament", "STRING"),
        bigquery.SchemaField(
            "weight",
            "RECORD",
            mode="NULLABLE",
            fields=[
                bigquery.SchemaField("imperial", "STRING"),
                bigquery.SchemaField("metric", "STRING"),
            ],
        ),
        bigquery.SchemaField(
            "height",
            "RECORD",
            mode="NULLABLE",
            fields=[
                bigquery.SchemaField("imperial", "STRING"),
                bigquery.SchemaField("metric", "STRING"),
            ],
        ),
        bigquery.SchemaField("reference_image_id", "STRING"),
        bigquery.SchemaField("country_code", "STRING"),
        bigquery.SchemaField("description", "STRING"),
        bigquery.SchemaField("history", "STRING"),
    ]
    dataset_ref = client.dataset(dataset_name)
    existing_table = dataset_ref.table(table_name)
    
    if existing_table is None:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)


def transfer_data_to_bigquery_table():
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    uri = f"gs://{bucket_name}/{destination_blob_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
    )

    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)

    load_job.result()

def run_daily_operations():
    """Runs all steps: Create Bucket, Upload Data, Create BigQuery Dataset, and Transfer Data."""
    create_gcp_bucket()
    create_bucket_object()
    create_bigquery_dataset()
    create_bigquery_table()
    transfer_data_to_bigquery_table()

if __name__ == "__main__":
    run_daily_operations()
