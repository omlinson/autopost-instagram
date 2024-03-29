import requests
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.image_video import get_last_frame

def sai_image_to_video(api_key, image_path, iterations):

    video_paths = []
    for i in range(iterations):

        i+=1

        cfg_scale = ((1.8/2)*(1+i/(iterations-1))) #default 1.8 max 10
        motion_bucket_id = 127*2 #max 255

        

        print(f"Generating video {i}...")
        print(f"cfg_scale: {cfg_scale}, motion_bucket_id: {motion_bucket_id}")

        response = requests.post(
            f"https://api.stability.ai/v2alpha/generation/image-to-video",
            headers={"authorization": f"Bearer {api_key}"},
            files={"image": open(image_path, "rb")},
            data={
                "seed": 0,
                "cfg_scale": {cfg_scale},
                "motion_bucket_id": {motion_bucket_id}
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        print("Generation ID:", response.json().get('id'))

        generation_id = response.json().get('id')
        retrieve_video(api_key, generation_id, i)
        video_paths.append(f"./temp/video_{i}.mp4")
        get_last_frame(f"./temp/video_{i}.mp4", i)
        image_path = f"./temp/lastframe_{i}.jpg"
    
    print("All videos generated!")

    return video_paths

def retrieve_video(api_key, generation_id, iteration):
    
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.request(
        "GET",
        f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
        headers={
            'Accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer {api_key}"
        },
    )

    if response.status_code == 202:
        print("Generation in-progress, try again in 10 seconds.")
        sleep(13)
        retrieve_video(api_key, generation_id, iteration)
    elif response.status_code == 200:
        print("Generation complete!")
        print("Generation seed:", response.headers.get('seed'))
        with open(f"./temp/video_{iteration}.mp4", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
