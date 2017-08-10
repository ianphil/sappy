from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials

KEY_VAULT_URI = 'https://<tmp>.vault.azure.net'

def auth_callack(server, resource, scope):
    data_creds = ServicePrincipalCredentials( 
            client_id = '',
            secret = '',
            tenant = '',
            resource = 'https://vault.azure.net'
        )
    token = data_creds.token
    return token['token_type'], token['access_token']

client = KeyVaultClient(KeyVaultAuthentication(auth_callack))

key_bundle = client.create_key(KEY_VAULT_URI, 'FirstKey', 'RSA')

print key_bundle
