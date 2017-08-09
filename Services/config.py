import json
from Models.secrets import Secrets

class Config:
    def __init__(self, secrets_filename):
        self.sec_file = secrets_filename

    def get_secrets(self):
        with open(self.sec_file) as secrets_file:
            data = json.load(secrets_file)
        
        secrets = Secrets()
        secrets.cosmos_endpoint = data['COSMOS_ENDPOINT']
        secrets.cosmos_master_key = data['COSMOS_MASTERKEY']
        secrets.documentdb_database = data['DOCUMENTDB_DATABASE']
        secrets.documentdb_collection = data['DOCUMENTDB_COLLECTION']
        secrets.spotify_client_id = data['SPOTIFY_CLIENT_ID']
        secrets.spotify_client_secret = data['SPOTIFY_CLIENT_SECRET']
        secrets.spotify_redirect_url = data['SPOTIFY_REDIRECT_URL']

        return secrets
