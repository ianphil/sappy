"""Used to scrape data"""
import wikipedia
import pydocumentdb
import pydocumentdb.document_client as document_client

config = {
    'ENDPOINT': 'https://<account_name>.documents.azure.com',
    'MASTERKEY': '<account_key>',
    'DOCUMENTDB_DATABASE': '<db_name',
    'DOCUMENTDB_COLLECTION': 'col_name'
}

client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
db = client.CreateDatabase({'id': config['DOCUMENTDB_DATABASE']})
collection = client.CreateCollection(db['_self'], {'id': config['DOCUMENTDB_COLLECTION']})

def get_big_hair_list():
    """Gets the list of bands and returns"""
    big_hair_list = wikipedia.page("List of glam metal bands and artists")
    return big_hair_list.links

for bh in get_big_hair_list():
    print "Adding: " + bh
    client.CreateDocument(collection['_self'], {'BandName': bh})
