"""Used to scrape data"""
import wikipedia
import json
import pydocumentdb
import pydocumentdb.document_client as document_client

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)

client = document_client.DocumentClient(secrets['ENDPOINT'], {'masterKey': secrets['MASTERKEY']})
db = client.CreateDatabase({'id': secrets['DOCUMENTDB_DATABASE']})
collection = client.CreateCollection(db['_self'], {'id': secrets['DOCUMENTDB_COLLECTION']})

def get_big_hair_list():
    """Gets the list of bands and returns"""
    big_hair_list = wikipedia.page("List of glam metal bands and artists")
    return big_hair_list.links

for bh in get_big_hair_list():
    print "Adding: " + bh
    client.CreateDocument(collection['_self'], {'BandName': bh})
