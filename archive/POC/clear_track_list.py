import json
import spotipy
import logging
from spotipy.oauth2 import SpotifyClientCredentials
from pydocumentdb import document_client

logging.basicConfig(filename="track.create.log", level=logging.DEBUG)

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

query = {"query": 'SELECT * FROM c WHERE c.Type = "Album"'}

options = {}
options["enableCrossPartitionQuery"] = True
options["maxItemCount"] = 2

results = client.QueryDocuments(coll["_self"], query, options)
# results = list(result_iterable)

count = 1
for album in results:
    try:
        album["Track_List"] = []
        client.UpsertDocument(coll["_self"], album)
    except:
        logging.error(" --- ERROR --- There was a problem")
