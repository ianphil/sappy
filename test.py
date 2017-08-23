from Services.keyvault import KeyVault
from Services.config import Config
import json

config = Config("secrets.json").get_secrets()

keyvault = KeyVault('https://bighair.vault.azure.net/', config)

# data = keyvault.create_key('secondkey', 'RSA')
# print(data)

# keys = keyvault.get_keys()

# for key in keys:
#     print(key)

# sec_id = keyvault.create_secret('yoyo', 'this could be')
# print(sec_id)

# data = keyvault.get_secret('yoyo')
# print(data)

sec_list = keyvault.get_secrets()
for sec in sec_list:
    print(sec)
    keyvault.delete_secret(sec.id.split('/')[-1])
