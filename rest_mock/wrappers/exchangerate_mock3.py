import requests
import random
from datetime import datetime as dt
from datetime import timedelta

class MockExchangeRate():

    def __init__(self):
        self.url = "http://www.mocky.io/v2/5e383a4c310000e389d3808d"

    def get(self, serialize = True):
        if serialize:
            return self.serializer(requests.get(self.url))
        else:
            return requests.get(self.url)

    def serializer(self,data):
        # Data serializer to match other providers
        serialized_data = []
        for i in data.json():
            serialized_data.append({'code':i['currency'],'rate':i['rate_mid']})
        return serialized_data

    def generate_random(self):
        # Since mocks doesnt return any timestamp info to calculate last 24 hours best rates i've created my own mock data.
        rates = [{'timestamp': (dt.now().replace(minute=0,second=0,microsecond=0) - timedelta(hours= 24 - i)).timestamp(),
                  'eur': random.uniform(4,6),
                  'usd': random.uniform(4,5.5),
                  'gbp': random.uniform(5,7)} for i in range(24)]

        return rates