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

for doc in client.ReadDocuments(coll["_self"]):
    results = spotify.search(q="artist:" + doc["Band_Name"], type="artist")

    for item in results["artists"]["items"]:
        if item["name"] == doc["Band_Name"]:
            print "Updating Band: " + doc["Band_Name"]
            doc["Spotify_Url"] = item["uri"]
            if item["images"]:
                doc["Spotify_Image_Url"] = item["images"][0]["url"]
            doc["Spotify_Popularity"] = item["popularity"]
            doc["Spotify_Followers"] = item["followers"]["total"]
            doc["Spotify_Id"] = item["id"]
            doc["Spotify_External_Url"] = item["external_urls"]["spotify"]
            doc["Spotify_Genres"] = item["genres"]
            client.UpsertDocument(coll["_self"], doc)
            break
