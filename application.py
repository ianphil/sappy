from Services.keyvault import KeyVault
from Services.config import Config
from Services.wiki_data import WikiData
from Models.artist import Artist
from Models.my_encoder import MyEncoder
import json

config = Config("secrets.json").get_secrets()
wiki_data = WikiData('List of glam metal bands and artists')
artist_list = wiki_data.get_page_links()

count = 1
for a in artist_list:
    artist = Artist()
    artist.artist_id = count
    artist.name = a

    print(MyEncoder().encode(artist))
    count += 1
