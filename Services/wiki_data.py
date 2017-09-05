import json
import wikipedia

class WikiData:
    def __init__(self, page_name):
        self.page_name = page_name
    
    def get_page_links(self):
        big_hair_list = wikipedia.page(self.page_name)
        return big_hair_list.links
