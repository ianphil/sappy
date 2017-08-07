import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydocumentdb import document_client

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

for album in results:
    print "Deleteing: " + album['Album_Name']
    client.DeleteDocument(album['_self'])

