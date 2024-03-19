def create_video_story_media_object(video_url):
    url = f'https://graph.facebook.com/v19.0/{instagram_business_id}/media'
    payload = {
        'video_url': video_url,
        'access_token': access_token
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  
        return response.json().get('id')
    except requests.exceptions.RequestException as e:
        print(f"Error creating media object: {e}")
        return None

def publish_media_object(container_id):
    url = f'https://graph.facebook.com/v19.0/{instagram_business_id}/media_publish'
    payload = {
        'creation_id': container_id,
        'access_token': access_token
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error publishing media object: {e}")
        return None
