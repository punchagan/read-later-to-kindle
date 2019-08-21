import json
import os
import tempfile

import requests

TOKEN = os.environ["API_TOKEN"]
BASE_URL = "https://api.pinboard.in/v1/posts"


class PinboardQueueConsumer:
    """Fetches unread items from Pinboard"""

    def __init__(self):
        self.session = requests.Session()

    def get_last_unread(self, n=25):
        """Return the last n unread items from Pinboard"""
        return self._all_items[-n:]

    @property
    def update_time(self):
        url = "{}/update?auth_token={}&format=json".format(BASE_URL, TOKEN)
        response = self.session.get(url)
        return response.json()["update_time"]

    @property
    def _all_items(self):
        filename = "pinboard-cache-{}".format(self.update_time)
        cache_path = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(cache_path):
            with open(cache_path) as f:
                data = json.load(f)
        else:
            data = self._fetch_all_items()
            with open(cache_path, "w") as f:
                json.dump(data, f, indent=1)

        return data

    def _fetch_all_items(self):
        url = "{}/all?auth_token={}&format=json&toread=yes".format(
            BASE_URL, TOKEN
        )
        response = self.session.get(url)
        return response.json()
