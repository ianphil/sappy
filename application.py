from Services.config import Config
from Services.wiki_data import WikiData
from Services.cosmosdb import CosmosDb
from Services.cognitive_services import Cognitive_Services
from Services.logger import Logger
from Services.spotify import Spotify
from Services.genius_lyrics import Lyrics
from Models.artist import Artist
from Models.album import Album
import json
import time

config = Config("secrets.json").get_secrets()
db = CosmosDb(config)
spotify_client = Spotify(config)
logger = Logger('/tmp/sappy.log', 'DEBUG')
wiki = WikiData("List of glam metal bands and artists")

def Save_Artists(artist_names):
    for artist in artist_names:
        try:
            logger.log_info("Getting Artist info for: " + artist.name)
            artist_data = spotify_client.get_artist_info(artist)
            for a in artist_data['artists']['items']:
                spotify_artist = Artist()

                spotify_artist.name = a['name']
                spotify_artist.spotify_external_url = a['external_urls']['spotify']
                spotify_artist.spotify_followers = a['followers']['total']
                spotify_artist.spotify_genres = a['genres']
                spotify_artist.spotify_id = a['id']

                if a['images']:
                    spotify_artist.spotify_image_url = a['images'][0]['url']

                spotify_artist.spotify_popularity = a['popularity']
                spotify_artist.spotify_url = a['uri']

                logger.log_info("Creating " + artist.name)

                try:
                    db.insert(spotify_artist)
                except Exception as ex:
                    logger.log_error("CosmosDB Insert Artist: " + a['name'] + " -- " + ex)

        except Exception as ex:
            logger.log_error("Spotify Get Artist Info: " + artist.name + " -- " + ex)

def create_album(a, count, artist_id):
    album = Album()
    album.album_id = count
    album.artist_id = artist_id
    album.spotify_external_url = a['external_urls']['spotify']
    album.spotify_id = a['id']
    album.spotify_url = a['uri']
    album.spptify_image_url = a['images'][0]['url']
    album.name = a['name']
    return album

def main():
    # artist_names = wiki.get_artist_names()
    # Save_Artists(artist_names)

    # TODO: Get Albums & save
    count = 1
    for artist in db.get_artists():
        spotify_album_list = spotify_client.get_artist_album_list(artist)
        for album in spotify_album_list['items']:
            a = create_album(album, count, artist.artist_id)
            count += 1
        
    # TODO: Get Songs & save

if __name__ == "__main__": 
    main()
