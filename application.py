from Services.config import Config
from Services.wiki_data import WikiData
from Services.cosmosdb import CosmosDb
import json

config = Config("secrets.json").get_secrets()
# wiki_data = WikiData('List of glam metal bands and artists')
# artist_list = wiki_data.get_artist_names()
cosmos = CosmosDb(config)

# for artist in artist_list:
#     cosmos.insert(artist)

db_artists = cosmos.get_artists()
