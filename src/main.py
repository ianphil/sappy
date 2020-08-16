#!/usr/bin/env python
import os
import json
import spotipy
import constants
import wikipedia
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# TODO: Need to do better clean up... whitesnake!


if __name__ == "__main__":
    gather_data = False
    get_scores = False

    if gather_data:
        # Get artists from Wikipedia
        wiki_artists = [
            {"name": link.split("(")[0].rstrip()}
            for link in wikipedia.page("List of glam metal bands and artists").links
        ]

        # Get artists and track from the 80s with track thats in Aritist's list of top
        # 10 played tracks on Spotify
        spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

        spotify_artists = [
            spotify_client.search(
                q=f'artist:{artist["name"]} year:1980-1989', type="artist"
            )
            for artist in wiki_artists
        ]

        artists_that_exist = [
            artist["artists"]["items"][0]
            for artist in spotify_artists
            if len(artist["artists"]["items"]) != 0
        ]

        artists_with_top_10_tracks = [
            spotify_client.artist_top_tracks(artist["id"])
            for artist in artists_that_exist
        ]

        artists_with_top_80s_track = []
        for artist in artists_with_top_10_tracks:
            for track in artist["tracks"]:
                if 1980 <= int(track["album"]["release_date"].split("-")[0]) < 1990:
                    artists_with_top_80s_track.append(track)
                    break

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

        with open("src/store/lyrics.json", "w") as lyrics:
            json.dump(lyric_list, lyrics)

    # Get sentiment for each track
    if get_scores:
        with open("src/store/lyrics.json", "r") as lyrics:
            song_list = json.load(lyrics)

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

        with open("src/store/lyrics.json", "w") as lyrics:
            json.dump(song_list, lyrics)

    # Sort [rank] by sentiment
    with open("src/store/lyrics.json", "r") as lyrics:
        scored_song_list = json.load(lyrics)

    sorted_list = sorted(
        scored_song_list,
        key=lambda x: (x["score"]["positive"], x["score"]["negative"]),
        reverse=True,
    )

    with open("src/store/lyrics.json", "w") as lyrics:
        json.dump(sorted_list, lyrics)
