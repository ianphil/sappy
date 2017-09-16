import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
    def __init__(self, config):
        self.config = config
        self.spotify_creds = SpotifyClientCredentials(config.spotify_client_id, config.spotify_client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.spotify_creds)

    def get_artist_info(self, artist):
        results = self.spotify.search(q='artist:' + artist.name, type='artist')
        return results

    def get_artist_album_list(self, artist):
        results = self.spotify.artist_albums(artist.spotify_id)
        return results

    def get_album_info(self, album):
        results = self.spotify.album(album.spotify_id)
        return results

    def get_album_track_list(self, album):
        results = self.spotify.album(album.spotify_id)
        return results