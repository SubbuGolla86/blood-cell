from google.cloud import  storage

storage_client = storage.Client()
bucket_name = " blood_cell_bucket"
bucket = storage_client.bucket(bucket_name)

def upload_file(file_name):
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    return

def download_file(file_name):
    image_blob = bucket.blob(file_name)
    image_blob.download_to_filename(file_name)
