"""Used to scrape data"""
import wikipedia
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

collection = client.CreateCollection(
    db["_self"], {"id": secrets["DOCUMENTDB_COLLECTION"]}
)


def get_big_hair_list():
    """Gets the list of bands and returns"""
    big_hair_list = wikipedia.page("List of glam metal bands and artists")
    return big_hair_list.links


count = 1
for bh in get_big_hair_list():
    print "Adding: " + bh
    client.CreateDocument(
        collection["_self"], {"Band_Id": count, "Band_Name": bh, "Album_List": []}
    )
    count += 1
