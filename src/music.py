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

        offset = 0
        while True:
            results = self._client.search(q=query, type="artist", offset=offset)[
                "artists"
            ]

            for band in results["items"]:
                yield band

            offset = offset + len(results["items"])
            if len(results["items"]) == 0:
                break

    def get_artists_top_ten_tracks(self, artists):
        """returns a list of top 10 tracks for all artists passed to method"""
        return (self._client.artist_top_tracks(artist["id"]) for artist in artists)

    def get_artists_top_track_from_years(self, artists, **kwargs):
        """Returns only the top track from given year or year range. Accepts kwargs
        year [int] or year_range [tuple[int]]."""
        for artist in artists:
            if "year" in kwargs.keys():
                yield from self._get_from_year(artist["tracks"], kwargs["year"])

            if "year_range" in kwargs.keys():
                yield from self._get_from_year_range(
                    artist["tracks"], kwargs["year_range"]
                )

    def _get_from_year(self, tracks, year):
        for track in tracks:
            if int(track["album"]["release_date"].split("-")[0]) == year:
                yield track
                break

    def _get_from_year_range(self, tracks, year_range):
        for track in tracks:
            if (
                year_range[0]
                <= int(track["album"]["release_date"].split("-")[0])
                <= year_range[1]
            ):
                yield track
                break
