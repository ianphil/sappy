import requests
from bs4 import BeautifulSoup


class Lyrics:
    def __init__(self, config):
        self.config = config
        self.base_url = "http://api.genius.com"
        self.headers = {"Authorization": "Bearer " + self.config.genius_sec}

    def lyrics_from_song_api_path(self, song_api_path):
        song_url = self.base_url + song_api_path
        response = requests.get(song_url, headers=self.headers)
        json = response.json()
        path = json["response"]["song"]["path"]
        # gotta go regular html scraping... come on Genius
        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")
        # remove script tags that they put in the middle of the lyrics
        [h.extract() for h in html("script")]
        # at least Genius is nice and has a tag called 'lyrics'!
        lyrics = html.find(
            "div", class_="lyrics"
        ).get_text()  # updated css where the lyrics are based in HTML
        return lyrics

    def get_lyrics(self, artist_name, song_title):
        search_url = self.base_url + "/search?q=" + song_title
        response = requests.get(search_url, headers=self.headers)
        json = response.json()
        song_info = None
        for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"] == artist_name:
                song_info = hit
                break
        if song_info:
            song_api_path = song_info["result"]["api_path"]
            return self.lyrics_from_song_api_path(song_api_path)
