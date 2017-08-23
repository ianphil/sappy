from azure.keyvault import KeyVaultClient, KeyVaultId
from azure.common.credentials import ServicePrincipalCredentials

class KeyVault:
    def __init__(self, uri, config):
        self.keyvault_uri = uri
        self.config = config
        self.client = KeyVaultClient(ServicePrincipalCredentials(client_id=self.config.client_id,
                                                                 secret=self.config.client_secret,
                                                                 tenant=self.config.tenant_id))
 
    def create_key(self, key_name, key_type):
        key_bundle = self.client.create_key(self.keyvault_uri, key_name, key_type)
        key_id = KeyVaultId.parse_key_id(key_bundle.key.kid)
        return key_id

    def get_keys(self):
        key_list = self.client.get_keys(self.keyvault_uri)
        return key_list

    def delete_key(self, name):
        deleted_key = self.client.delete_key(self.keyvault_uri, name)
        return deleted_key

    def create_secret(self, name, secret):
        secret_bundle = self.client.set_secret(self.keyvault_uri, name, secret)
        secret_id = KeyVaultId.parse_secret_id(secret_bundle.id)
        return secret_id

    def get_secrets(self):
        secret_list = self.client.get_secrets(self.keyvault_uri)
        return secret_list

    def get_secret(self, name, version = ''):
        secret = self.client.get_secret(self.keyvault_uri, name, version)
        return secret.value

    def delete_secret(self, name):
        deleted_secret = self.client.delete_secret(self.keyvault_uri, name)
        return deleted_secret
