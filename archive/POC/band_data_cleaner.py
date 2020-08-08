"""This removes the (Band) appended to some of the names"""
import json
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

for doc in client.ReadDocuments(coll["_self"]):
    # if doc['Spotify_Url'] == []: #(287 - 202) record count
    # if doc['Spotify_Genres'] == []: #(202 - 172)
    #     print "Deleting Band: " + doc["Band_Name"]
    #     client.DeleteDocument(doc['_self'])
    # print "Updating Band: " + doc["Band_Name"]
    # doc["Band_Name"] = doc["Band_Name"].split("(")[0]
    # doc["Band_Name"] = doc["Band_Name"].rstrip()
    doc["Type"] = "Band"
    client.UpsertDocument(coll["_self"], doc)
