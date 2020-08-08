import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

client_credentials_manager = SpotifyClientCredentials(
    secrets["SPOTIFY_CLIENT_ID"], secrets["SPOTIFY_CLIENT_SECRET"]
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = "Aerosmith"
results = spotify.search(q="artist:" + name, type="artist")

for item in results["artists"]["items"]:
    print item["name"]
