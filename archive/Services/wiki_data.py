import json
import wikipedia
from Models.artist import Artist


class WikiData:
    def __init__(self, page_name):
        self.page_name = page_name

    def get_artist_names(self):
        big_hair_list = wikipedia.page(self.page_name)

        # Clean the data in place
        del big_hair_list.links[0:3]
        big_hair_list.links.pop(145)
        big_hair_list.links.pop(146)

        artist_list = []
        count = 1
        for link in big_hair_list.links:
            link = link.split("(")[0].rstrip()
            artist = Artist()
            artist.artist_id = count
            artist.name = link
            artist_list.append(artist)
            count += 1

        return artist_list
