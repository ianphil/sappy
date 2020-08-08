import json
import urllib
import http.client


class Cognitive_Services:
    def __init__(self, config):
        self.config = config

    def get_sentiment(self, document):
        "Gets the sentiments for a set of documents and returns the information."

        doc = {"documents": [{"id": "1", "language": "en", "text": document}]}

        headers = {"Ocp-Apim-Subscription-Key": self.config.cog_svc_sec}
        conn = http.client.HTTPSConnection(self.config.cog_svc_host)
        body = json.dumps(doc)
        conn.request("POST", self.config.cog_svc_path, body, headers)
        response = conn.getresponse()
        data = response.read()
        pyList = json.loads(data)
        score = str(pyList["documents"][0]["score"])
        return score
