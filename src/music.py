#!/usr/bin/env python
import os
import spotipy
import lyricsgenius
from time import sleep
from requests import ReadTimeout
from constants import GENIUS_CLIENT_TOKEN
from spotipy.oauth2 import SpotifyClientCredentials


class MusicProvider:
    """Collects Music data we are going to work with"""

    def __init__(self):
        self._client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self._lyric_client = lyricsgenius.Genius(
            os.getenv(GENIUS_CLIENT_TOKEN), verbose=False
        )

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
                yield from _get_from_year(artist["tracks"], kwargs["year"])

            if "year_range" in kwargs.keys():
                yield from _get_from_year_range(artist["tracks"], kwargs["year_range"])

    def get_lyrics_for_song(self, artists):
        for track in artists:
            try:
                song = self._song_search(
                    track["name"], artist=track["artists"][0]["name"]
                )
            except ReadTimeout as t:
                _backoff(t)
                song = self._song_search(
                    track["name"], artist=track["artists"][0]["name"]
                )
            except TypeError as t:
                pass

            if song is not None:
                yield {
                    "artist": song.artist,
                    "songTitle": song.title,
                    "lyrics": song.lyrics,
                }

    def _song_search(self, track, artist):
        _be_nice()
        return self._lyric_client.search_song(track, artist=artist)


def _be_nice():
    sleep(0.100)


def _backoff(log_msg):
    sleep(0.700)


def _get_from_year(tracks, year):
    for track in tracks:
        if int(track["album"]["release_date"].split("-")[0]) == year:
            yield track
            break


def _get_from_year_range(tracks, year_range):
    for track in tracks:
        if (
            year_range[0]
            <= int(track["album"]["release_date"].split("-")[0])
            <= year_range[1]
        ):
            yield track
            break
