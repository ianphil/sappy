import json
from Models.secrets import Secrets
from Services.keyvault import KeyVault


class Config:
    def __init__(self, secrets_filename):
        self.sec_file = secrets_filename

    def get_secrets(self):
        with open(self.sec_file) as secrets_file:
            data = json.load(secrets_file)

        secrets = Secrets()
        secrets.cosmos_endpoint = data["COSMOS_ENDPOINT"]
        secrets.cosmos_master_key_name = data["COSMOS_MASTERKEY_NAME"]
        secrets.documentdb_database = data["DOCUMENTDB_DATABASE"]
        secrets.documentdb_collection = data["DOCUMENTDB_COLLECTION"]
        secrets.spotify_client_id = data["SPOTIFY_CLIENT_ID"]
        secrets.spotify_client_secret_name = data["SPOTIFY_CLIENT_SECRET_NAME"]
        secrets.spotify_redirect_url = data["SPOTIFY_REDIRECT_URL"]
        secrets.client_id = data["client_id"]
        secrets.client_secret = data["client_secret"]
        secrets.tenant_id = data["tenant_id"]
        secrets.keyvault_url = data["keyvault_url"]
        secrets.cog_svc_host = data["cog_svc_host"]
        secrets.cog_svc_path = data["cog_svc_path"]
        secrets.cog_svc_sec = data["cog_svc_sec"]
        secrets.genius_sec = data["genius_sec"]

        keyvault = KeyVault(secrets.keyvault_url, secrets)
        secrets.cosmos_master_key = keyvault.get_secret(secrets.cosmos_master_key_name)
        secrets.spotify_client_secret = keyvault.get_secret(
            secrets.spotify_client_secret_name
        )

        return secrets
