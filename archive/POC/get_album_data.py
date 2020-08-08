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

query = {
    "query": 'SELECT c.Band_Name, c.Spotify_Id, c.Band_Id FROM c WHERE c.Type = "Band"'
}

options = {}
options["enableCrossPartitionQuery"] = True
options["maxItemCount"] = 2

result_iterable = client.QueryDocuments(coll["_self"], query, options)
results = list(result_iterable)

count = 1
for band in results:
    album_list = spotify.artist_albums(band["Spotify_Id"])
    for album in album_list["items"]:
        if "US" in album["available_markets"]:
            try:
                print "Creating: " + album["name"] + " for: " + band["Band_Name"]
                client.CreateDocument(
                    coll["_self"],
                    {
                        "Album_Id": count,
                        "Type": "Album",
                        "Album_Name": album["name"],
                        "Band_Id": band["Band_Id"],
                        "Track_List": [],
                        "Spotify_External_Url": album["external_urls"]["spotify"],
                        "Spotify_Id": album["id"],
                        "Spotify_Image_Url": album["images"][0]["url"],
                        "Spotify_Url": album["uri"],
                    },
                )
                count += 1
            except:
                print " --- ERROR --- Band: " + band["Band_Name"]
