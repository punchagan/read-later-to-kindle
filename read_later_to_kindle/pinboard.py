import json
import os
import tempfile

import requests

TOKEN = os.environ["API_TOKEN"]
BASE_URL = "https://api.pinboard.in/v1/posts"


class PinboardQueueConsumer:
    """Fetches unread items from Pinboard"""

    def __init__(self, num_unread=25):
        self.session = requests.Session()
        self.num_unread = num_unread

    def get_last_unread(self):
        """Return the last n unread items from Pinboard"""
        n = self.num_unread
        return self._all_items[-n:][::-1]

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

        self._add_mark_as_read_url(data)
        return data

    def _fetch_all_items(self):
        url = "{}/all?auth_token={}&format=json&toread=yes".format(
            BASE_URL, TOKEN
        )
        response = self.session.get(url)
        return response.json()

    def _add_mark_as_read_url(self, entries):
        for entry in entries:
            params = "url={href}&description={description}".format(**entry)
            mark_as_read_url = "{base_url}/add?auth_token={token}&format=json&{params}".format(
                base_url=BASE_URL, token=TOKEN, params=params
            )
            entry["mark_as_read"] = mark_as_read_url
