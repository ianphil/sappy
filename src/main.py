#!/usr/bin/env python
import spotipy
import wikipedia
from spotipy.oauth2 import SpotifyClientCredentials


if __name__ == "__main__":
    client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    # Get artists from Wikipedia
    artists = [
        {"name": link.split("(")[0].rstrip()}
        for link in wikipedia.page("List of glam metal bands and artists").links
    ]

    # Get artists top track in the 80s
    for artist in artists:
        track = client.search(f'q=artist:{artist["name"]}%20year:1980-1989&type=track')
        print(track)
    # Get Top track lyrics
    # Get sentiment for each track
    # Sort [rank] by sentiment
