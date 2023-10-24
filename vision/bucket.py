import json
import re
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

from google.cloud import vision
from google.cloud import storage

def delete_existing_results(gcs_destination_uri):
    storage_client = storage.Client()
    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    bucket = storage_client.get_bucket(bucket_name)

    # List and delete objects with the given prefix
    for blob in list(bucket.list_blobs(prefix=prefix)):
        blob.delete()

def async_detect_document(local_file_path, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    import json
    import re
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

    from google.cloud import vision
    from google.cloud import storage

    # Set your GCS bucket and object name for the uploaded file
    gcs_bucket_name = 'autograde_files'
    gcs_object_name = 'Doc2.pdf'  # Change to the desired object name

    # Initialize a GCS client
    storage_client = storage.Client()

    # Upload the local file to GCS
    bucket = storage_client.get_bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_object_name)
    blob.upload_from_filename(local_file_path)

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "application/pdf"

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source_uri = f"gs://{gcs_bucket_name}/{gcs_object_name}"
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]
    print("Output files:")
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_bytes().decode("utf-8")
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    first_page_response = response["responses"][0]
    annotation = first_page_response["fullTextAnnotation"]

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print("Full text:\n")
    print(annotation["text"])

# Replace these paths with your local file path and GCS destination URI
local_file_path = "Doc2.pdf"
gcs_destination_uri = "gs://autograde_files/results"

delete_existing_results(gcs_destination_uri)
async_detect_document(local_file_path, gcs_destination_uri)
