import requests

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

urls = ["https://glorious-goggles-q69x77g49g5fx7xx-8000.app.github.dev/key.7z", "https://glorious-goggles-q69x77g49g5fx7xx-8000.app.github.dev/Screenshots.zip"]
for url in urls:
    download_file(url)