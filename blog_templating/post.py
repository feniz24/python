import requests


class Post:
    def __init__(self):
        self.url = "https://api.npoint.io/271ef9ccbbdb9eefc57f"

    def get_post(self):
        response = requests.get(self.url)
        all_posts = response.json()
        return all_posts

