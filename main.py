import os
from dotenv import load_dotenv
from google.cloud import storage
from utils.image_video import square_image, merge_videos
from utils.gcp import get_random_image
from utils.stabilityai import sai_image_to_video


# Settings

post_type= "story"
iterations = 2 # Number of videos to generate and stich together
min_square = 768 # Minimum size of the square for stabilty    
resize = "1280x720" # Resolution of the video
#end_card = "./temp/endcard.jpg"
end_card = False
return_to_source = True # Return to the original image at the end of the video

# Load environment variables
load_dotenv()

# Set up Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
storage_client = storage.Client()
gcs_bucket_name = os.getenv('GCS_BUCKET_NAME')

#Set up AI

sai_api_key = os.getenv("STABILITY_API_KEY")

# Get a random image from GCS and resize.
# Should eventually be logged in Google Sheets.

#image_path = get_random_image(gcs_bucket_name, storage_client)
#image_path = r"./temp/random_image.jpg" 

#image_path = square_image(image_path, min_square)
image_path = r"./temp/resized_image.jpg"

# Create content based on media type

if post_type == "story":

    print("Creating story...")
    #video_paths = sai_image_to_video(sai_api_key, image_path, iterations)
    video_paths = [r"./temp/video_1.mp4", r"./temp/video_2.mp4"]
    image_path = r"./temp/resized_image.jpg" #not sure if this is necessary    
    main_video_path = merge_videos(video_paths, image_path, return_to_source, end_card) #not currently working
    
    # Generate background
    # Generate text
    # Stitch together    

else:

    print("Creating post...")

    # Generate caption
    # Should have carousel if end card is true

    pass


# Create media

# Publish media

print("Done!")




