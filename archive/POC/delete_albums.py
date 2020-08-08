import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydocumentdb import document_client

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

client = document_client.DocumentClient(
    secrets["COSMOS_ENDPOINT"], {"masterKey": secrets["COSMOS_MASTERKEY"]}
)
db = next(
    (
        data
        for data in client.ReadDatabases()
        if data["id"] == secrets["DOCUMENTDB_DATABASE"]
    )
)
coll = next(
    (
        coll
        for coll in client.ReadCollections(db["_self"])
        if coll["id"] == secrets["DOCUMENTDB_COLLECTION"]
    )
)

client_credentials_manager = SpotifyClientCredentials(
    secrets["SPOTIFY_CLIENT_ID"], secrets["SPOTIFY_CLIENT_SECRET"]
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

query = {"query": 'SELECT * FROM c WHERE c.Type = "Track"'}

options = {}
options["enableCrossPartitionQuery"] = True
options["maxItemCount"] = 2

results = client.QueryDocuments(coll["_self"], query, options)

for track in results:
    print "Deleteing: " + track["Track_Name"]
    client.DeleteDocument(track["_self"])
