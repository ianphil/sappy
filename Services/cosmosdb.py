from pydocumentdb import document_client
from Models.artist import Artist
from json import JSONEncoder

class CosmosDb:
    def __init__(self, config):
        self.config = config
        self.client = document_client.DocumentClient(
            config.cosmos_endpoint, {'masterKey': config.cosmos_master_key}
        )

        self.database = next((data for data in self.client.ReadDatabases()
            if data['id'] == config.documentdb_database)
        )

        self.collection = next((
            coll for coll in self.client.ReadCollections(self.database['_self']) 
            if coll['id'] == config.documentdb_collection)
        )

    def insert(self, entity):
        data = entity.__dict__
        self.client.CreateDocument(self.collection['_self'], data)

    def get_artists(self):
        artist_list = []
        for doc in self.client.ReadDocuments(self.collection['_self']):
            artist = Artist()
            artist.ctor_from_dict(**doc)
            artist_list.append(artist)

        return artist_list