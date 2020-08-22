#!/usr/bin/env python
import os
import constants
import lyricsgenius
from music import MusicProvider
from storage import LocalJsonFile
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# TODO: Need to do better clean up... whitesnake!


if __name__ == "__main__":
    gather_data = True
    get_scores = False

    storage_provider = LocalJsonFile()

    if gather_data:

        # Get artists and track from the 80s with track thats in Aritist's list of top
        # 10 played tracks on Spotify
        music = MusicProvider()
        artists = music.search_artist_by_genre("glam metal", year="1980-1989")
        artists_with_top_10_tracks = music.get_artists_top_ten_tracks(artists)
        artists_with_top_80s_track = music.get_artists_top_track_from_years(
            artists_with_top_10_tracks, year_range=(1980, 1989)
        )

        # Get Top track lyrics
        genius_client = lyricsgenius.Genius(
            os.getenv(constants.GENIUS_CLIENT_TOKEN), verbose=False
        )

        lyric_list = []
        for track in artists_with_top_80s_track:
            song = genius_client.search_song(
                track["name"], artist=track["artists"][0]["name"]
            )
            if song is not None:
                lyric_list.append(
                    {
                        "artist": song.artist,
                        "songTitle": song.title,
                        "lyrics": song.lyrics,
                    }
                )

        storage_provider.create(lyric_list)

    # Get sentiment for each track
    if get_scores:
        song_list = storage_provider.read()

        text_analytics_key = os.getenv(constants.TEXT_ANALYTICS_KEY)
        text_analytics_endpoint = os.getenv(constants.TEXT_ANALYTICS_ENDPOINT)

        text_analytics_cred = AzureKeyCredential(text_analytics_key)
        text_analytics_client = TextAnalyticsClient(
            endpoint=text_analytics_endpoint, credential=text_analytics_cred
        )

        for song in song_list:
            response = text_analytics_client.analyze_sentiment(
                documents=[song["lyrics"]]
            )[0]
            song["score"] = {
                "positive": response["confidence_scores"]["positive"],
                "neutral": response["confidence_scores"]["neutral"],
                "negative": response["confidence_scores"]["negative"],
            }

        storage_provider.create(song_list)

    # Sort [rank] by sentiment
    scored_song_list = storage_provider.read()

    sorted_list = sorted(
        scored_song_list,
        key=lambda x: (x["score"]["positive"], x["score"]["negative"]),
        reverse=True,
    )

    storage_provider.create(sorted_list)
