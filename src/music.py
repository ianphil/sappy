#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class MusicProvider:
    """Collects Music data we are going to work with"""

    def __init__(self):
        self._client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    def search_artist_by_genre(self, genre, **kwargs):
        """Searches for artists in a specific genre over specific year"""

        if "year" in kwargs.keys():
            query = f'genre: "{genre}" year:{kwargs["year"]}'
        else:
            query = f'genre: "{genre}"'

        bands = []
        offset = 0
        while True:
            results = self._client.search(q=query, type="artist", offset=offset)[
                "artists"
            ]
            [bands.append(band) for band in results["items"]]
            offset = offset + len(results["items"])
            if len(results["items"]) == 0:
                break
        return bands

    def get_artists_top_ten_tracks(self, artists):
        """returns a list of top 10 tracks for all artists passed to method"""
        return [self._client.artist_top_tracks(artist["id"]) for artist in artists]
