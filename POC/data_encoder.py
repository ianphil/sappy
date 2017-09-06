from json import JSONEncoder

class DataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
