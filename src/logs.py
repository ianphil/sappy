#!/usr/bin/env python
import os
import sys
import logging
from constants import LOGGING_MODE


class DangGoodLogProvider:
    """Contains logic for choosing log service and messages to log"""

    def __init__(self):
        mode = os.getenv(LOGGING_MODE)

        if mode == "Console":
            self._logger = ConsoleLoggerService.get()

        if mode == "File":
            self._logger = FileLoggerService.get()

    def artist_from_genre_search(self, band):
        msg = f'MusicProvider.search_artist_by_genre - {band["name"]}'
        self._logger.info(msg)

    def song_lyrics_error(self, artist_name, song_artist, song_name):
        e = "ERROR - "
        m = f"{artist_name.upper()} != {song_artist.upper()} -- {song_name}"
        msg = f"{e}{m}"
        self._logger.info(msg)

    def genre_search_failed(self, query):
        msg = f"ERROR - Genre Search {query}"
        self._logger.info(msg)

    def total_count_from_genre_search(self, count):
        msg = f"Total count from search - {count}"
        self._logger.info(msg)

    def top_tracks_failed(self, artist):
        msg = f'ERROR - Getting top 10 tracks for {artist["name"]}'
        self._logger.info(msg)

    def top_tracks_for_artist(self, artist):
        msg = f'Top 10 tracks for {artist["name"]} received'
        self._logger.info(msg)


class ConsoleLoggerService:
    """Create a specific stdout logger for sappy, so we don't have to deal with other
    packages logs."""

    @staticmethod
    def get():
        logger = logging.getLogger("sappy.console")
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(_get_formatter())
        logger.addHandler(ch)

        return logger


class FileLoggerService:
    """Create a specific file logger for sappy, so we don't have to deal with other
    packages logs."""

    @staticmethod
    def get():
        logger = logging.getLogger("sappy.file")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("sappy.log")
        fh.setFormatter(_get_formatter())
        logger.addHandler(fh)

        return logger


def _get_formatter():
    return logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
