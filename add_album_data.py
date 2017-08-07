import json
import spotipy
import logging
from spotipy.oauth2 import SpotifyClientCredentials
from pydocumentdb import document_client

logging.basicConfig(filename='album.update.log', level=logging.DEBUG)

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

client = document_client.DocumentClient(secrets['COSMOS_ENDPOINT'], {'masterKey': secrets['COSMOS_MASTERKEY']})
db = next((data for data in client.ReadDatabases() if data['id'] == secrets["DOCUMENTDB_DATABASE"]))
coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == secrets["DOCUMENTDB_COLLECTION"]))

client_credentials_manager = SpotifyClientCredentials(secrets["SPOTIFY_CLIENT_ID"], secrets["SPOTIFY_CLIENT_SECRET"])
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

query = { 'query': 'SELECT * FROM c WHERE c.Type = "Album"' }    

options = {} 
options['enableCrossPartitionQuery'] = True
options['maxItemCount'] = 2

result_iterable = client.QueryDocuments(coll['_self'], query, options)
results = list(result_iterable)

count = 1
for album in results:
    try:
        sp_album = spotify.album(album['Spotify_Id'])
        album['Label'] = sp_album['label']
        album['Popularity'] = sp_album['popularity']
        album['Release_Date'] = sp_album['release_date']
        logging.info('Updating album: ' + album['Album_Name'])
        print 'Updating album: ' + album['Album_Name']
        client.UpsertDocument(coll['_self'], album)
        # for track in sp_album['tracks']['items']:
        #     logging.info('Creating track: ' + track['name'])
        #     print 'Creating track: ' + track['name']
            # client.CreateDocument(coll["_self"], 
            #     {
            #         'Track_Id': count,
            #         'Type': 'Track',
            #         'Track_Name': track['name'],
            #         'Album_Id': album['Album_Id'],
            #         'Band_Id': album['Band_Id'],
            #         'Lyrics': [],
            #         'Total_Score': 0,
            #         'Disk_Number': track['disk_number'],
            #         'Duration_Ms': track['duration_ms'],
            #         'Explicit': track['explicit'],
            #         'Spotify_External_Url': track['external_urls']['spotify'],
            #         'Spotify_Id': track['id'],
            #         'Track_Number': track['track_number']
            #     })
            # count += 1
    except:
        logging.warning(' --- ERROR --- There was a problem')
