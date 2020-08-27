#!/usr/bin/env python
import os
import spotipy
import lyricsgenius
from time import sleep
from requests import ReadTimeout
from logs import DangGoodLogProvider
from constants import GENIUS_CLIENT_TOKEN
from spotipy.oauth2 import SpotifyClientCredentials


class MusicProvider:
    """Collects Music data we are going to work with"""

    def __init__(self):
        self._client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self._lyric_client = lyricsgenius.Genius(
            os.getenv(GENIUS_CLIENT_TOKEN), verbose=False
        )
        self._log = DangGoodLogProvider()

    def search_artist_by_genre(self, genre, **kwargs):
        """Searches for artists in a specific genre over specific year"""

        if "year" in kwargs.keys():
            query = f'genre: "{genre}" year:{kwargs["year"]}'
        else:
            query = f'genre: "{genre}"'

        offset = 0
        while True:
            try:
                results = self._client.search(q=query, type="artist", offset=offset)[
                    "artists"
                ]
            except:
                self._log.genre_search_failed(query)

            for band in results["items"]:
                yield band
                self._log.artist_from_genre_search(band)

            offset = offset + len(results["items"])
            if len(results["items"]) == 0:
                self._log.total_count_from_genre_search(offset)
                break

    def get_artists_top_ten_tracks(self, artists):
        """returns a list of top 10 tracks for all artists passed to method"""
        for artist in artists:
            try:
                top_tracks = self._client.artist_top_tracks(artist["id"])
            except:
                self._log.top_tracks_failed(artist)

            yield top_tracks
            self._log.top_tracks_for_artist(artist)

    def get_artists_top_track_from_years(self, artists, **kwargs):
        """Returns only the top track from given year or year range. Accepts kwargs
        year [int] or year_range [tuple[int]]."""
        for artist in artists:
            if "year" in kwargs.keys():
                yield from _get_from_year(artist["tracks"], kwargs["year"])

            if "year_range" in kwargs.keys():
                yield from _get_from_year_range(artist["tracks"], kwargs["year_range"])

    def get_lyrics_for_song(self, artists):
        # TODO Comment get_lyrics_for_song
        for track in artists:
            song_name = track["name"].split(" - ")[0].split(" (")[0]
            artist_name = track["artists"][0]["name"]
            try:
                song = self._song_search(song_name, artist=artist_name)
                # TODO add call_to_lyric_search
            except ReadTimeout as t:
                _backoff(t)
                song = self._song_search(song_name, artist=artist_name)
                # TODO add lyrics_timeout_error
            except TypeError as t:
                pass  # TODO add lyrics_type_error

            if song is not None:
                song_artist = song.artist.replace("’", "'").split(" (")[0]
                if artist_name.lower() == song_artist.lower():
                    yield {
                        "artist": artist_name,
                        "songTitle": song_name,
                        "lyrics": song.lyrics.replace("’", "'"),
                    }
                    # TODO add created_song
                else:
                    self._log.song_lyrics_error(artist_name, song_artist, song_name)

    def _song_search(self, track, artist):
        # TODO Comment _song_search
        # TODO Log _song_search
        _be_nice()
        return self._lyric_client.search_song(track, artist=artist)


def _be_nice():
    sleep(0.100)


def _backoff(log_msg):
    sleep(0.700)


def _get_from_year(tracks, year):
    # TODO comment get_from_year
    for track in tracks:
        if int(track["album"]["release_date"].split("-")[0]) == year:
            yield track
            # TODO add filter_track_by_year
            break


def _get_from_year_range(tracks, year_range):
    # TODO comment get_from_year_range
    for track in tracks:
        if (
            year_range[0]
            <= int(track["album"]["release_date"].split("-")[0])
            <= year_range[1]
        ):
            yield track
            # TODO add filter_track_by_year_range
            break
