import os
import requests
from werkzeug.utils import secure_filename
from urllib.parse import urlparse

def upload_image_from_url(url, storage_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        return "Invalid URL", 400

    # Check if the URL points to an image 
    if 'image' not in response.headers.get('Content-Type', ''):
        return "URL does not point to an image", 400

    # Create the storage path if it doesn't exist
    os.makedirs(storage_path, exist_ok=True)

    # Get the filename from the URL and make it safe
    filename = secure_filename(os.path.basename(urlparse(url).path))

    # Save the image to the storage path
    image_path = os.path.join(storage_path, filename)
    with open(image_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return "Image downloaded successfully", 200