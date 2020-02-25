import requests
import random
from datetime import datetime as dt
from datetime import timedelta


class MockExchangeRate():

    def __init__(self):
        self.url = "http://www.mocky.io/v2/5d19ec932f00004e00fd7326"


    def get(self , serialize = True):
        if serialize:
            return requests.get(self.url).json()
        else:
            return requests.get(self.url)

    def generate_random(self):
        # Since mocks doesnt return any timestamp info to calculate last 24 hours best rates i've created my own mock data.
        rates = [{'timestamp': (dt.now().replace(minute=0,second=0,microsecond=0) - timedelta(hours= 24 - i)).timestamp(),
                  'eur': random.uniform(4,6),
                  'usd': random.uniform(4,5.5),
                  'gbp': random.uniform(5,7)} for i in range(24)]

        return rates