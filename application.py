from Services.config import Config
from Services.wiki_data import WikiData
from Services.cosmosdb import CosmosDb
from Services.cognitive_services import Cognitive_Services
from Services.genius_lyrics import Lyrics
import json
import time

config = Config("secrets.json").get_secrets()

cog = Cognitive_Services(config)

lyrics = Lyrics(config).get_lyrics('Sia', 'Chandelier')
lyric_list = lyrics.splitlines()
for lyric in lyric_list:
    try:
        data = str(lyric).lstrip('[').rstrip(']')
        # time.sleep(1)
        score = cog.get_sentiment(str(data))
        print(data + ' -- score: ' + score)
    except Exception as ex:
        print(ex)
