import requests

def load_lottie_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
