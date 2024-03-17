import random
from google.cloud import storage
from utils.image_video import download_image


def get_random_image(bucket_name, storage_client):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = list(bucket.list_blobs(prefix="jpg/")) 
    jpg_blobs = [blob for blob in blobs if blob.name.lower().endswith('.jpg')]
    if jpg_blobs:
        selected_blob = random.choice(jpg_blobs)
        selected_blob_url = f"https://storage.googleapis.com/{bucket_name}/{selected_blob.name}"
        print(f"Selected image: {selected_blob_url}")
        image_path = download_image(selected_blob_url, r".\temp\random_image.jpg")
        return image_path
    else:
        return None

def upload_video_to_gcs(video_name, bucket_name, storage_client):
    # Upload the video to GCS

    destination_blob_name = f"video/{video_name}"
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(video_name)

    print("Uploaded video")

