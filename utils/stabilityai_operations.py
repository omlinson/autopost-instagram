
def generate_video(image_path):
    print("Generating video...")
    response = requests.post(
        f"https://api.stability.ai/v2alpha/generation/image-to-video",
        headers={"authorization": f"Bearer {api_key}"},
        files={"image": open(image_path, "rb")},
        data={
            "seed": 0,
            "cfg_scale": 1.8*0.85,
            "motion_bucket_id": 127*1.2
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    print("Generation ID:", response.json().get('id'))

    generation_id = response.json().get('id')

    return generation_id


def retrieve_video(generation_id, iteration):
    
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = requests.request(
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
        retrieve_video(generation_id, iteration)
    elif response.status_code == 200:
        print("Generation complete!")
        with open(f"video_{iteration}.mp4", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
