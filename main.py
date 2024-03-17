import os
from dotenv import load_dotenv
from google.cloud import storage
from utils.image_video import resize_image
from utils.gcp import get_random_image


# Settings

iterations = 3 # Number of videos to generate and stich together
min_square = 768 # Minimum size of the square for stabilty    
resize = "1280x720" # Resolution of the video
add_end_card = True # endcard.jpg
return_to_source = True


# Load environment variables
load_dotenv()

# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
storage_client = storage.Client()
gcs_bucket_name = os.getenv('GCS_BUCKET_NAME')

# Get a random image from GCS and resize
image_path = get_random_image(gcs_bucket_name, storage_client)
resize_image(image_path, min_square)

