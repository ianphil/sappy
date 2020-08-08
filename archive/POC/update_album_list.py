import json
import logging
from pydocumentdb import document_client

logging.basicConfig(filename="artist.update_album_list.log", level=logging.DEBUG)

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

band_query = {"query": 'SELECT * FROM c WHERE c.Type = "Band"'}

options = {}
options["enableCrossPartitionQuery"] = True
options["maxItemCount"] = 2

band_list = client.QueryDocuments(coll["_self"], band_query, options)

for band in band_list:
    try:
        print "Starting on Band List: " + band["Band_Name"]
        logging.info("Starting on Band List: " + band["Band_Name"])
        album_query = {
            "query": 'SELECT * FROM c WHERE c.Type = "Album" AND c.Band_Id = '
            + str(band["Band_Id"])
        }

        options = {}
        options["enableCrossPartitionQuery"] = True
        options["maxItemCount"] = 2

        album_list = client.QueryDocuments(coll["_self"], album_query, options)

        for album in album_list:
            print "Updating Album List for: " + band["Band_Name"]
            logging.info("Updating Album List for: " + band["Band_Name"])
            band["Album_List"].append(album["Album_Id"])

        print band["Album_List"]
        logging.info(band["Album_List"])
        client.UpsertDocument(coll["_self"], band)
    except:
        logging.error(" --- ERROR --- There was a problem")
