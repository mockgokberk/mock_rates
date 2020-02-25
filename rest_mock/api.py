from . import models
from . import serializers
from rest_framework import  permissions,viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime as dt
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from .wrappers.exchangerate_mock1 import MockExchangeRate as provider1
from .wrappers.exchangerate_mock2 import MockExchangeRate as provider2
from .wrappers.exchangerate_mock3 import MockExchangeRate as extra_provider
import sys
from django.core.cache import cache
import json
from collections import defaultdict

class ExchangeRate(APIView):
    """
    endpoint: /api/exchange_rate
    parameter: provider
    ex: http://127.0.0.1:8000/api/exchange_rate?provider=exchangerate_mock3
    return: given provider rates
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        provider = request.query_params.get('provider', None)
        try:
            if provider: # If not given or not exists returns error.
                response = self.get_wrapper(provider)
                return Response(response)
            return Response({'Error': "No provider specified"})
        except ValueError as e:
            return Response({"Error": "Enter a valid provider"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": "Something went so wrong " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_wrapper(self,provider):
        if not cache.get(provider):  # checks cache
            if provider.startswith("exchangerate"):
                for k in list(sys.modules.items()): # loops through available providers to match the given provider
                    if k[0].split('.')[-1]==provider:
                        api = getattr(sys.modules[k[0]], "MockExchangeRate")
                        response = api().get() # api call
                        cache.set(provider, json.dumps(response), 600) # sets cache
                        return response
                raise ValueError("Enter a valid provider")
            else:
                raise ValueError("Enter a valid provider")
        else:
            print('cached')
            cache.touch(provider, 600)  # refresh cache timeout
            return json.loads(cache.get(provider))


class BestRate(APIView):
    """
    endpoint: /api/best_rate
    parameter: currency(optional)
    ex: http://127.0.0.1:8000/api/best_rate  || http://127.0.0.1:8000/api/best_rate?currency=eur
    return: best rate
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        currency = request.query_params.get('currency', None)
        try:
            response = self.best_rate()
            if currency: # if exists return given currency else all currencies
                return Response({'timestamp':response['timestamp'],currency:response[currency]})
            return Response(response)
        except KeyError as e:
            return Response({"Error":"Enter a valid currency eur,usd,gbp"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": "Something went so wrong " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def best_rate(self):
        if not cache.get('best_values'): # checks cache
            best_values = defaultdict(int)
            best_values['timestamp'] = dt.now().timestamp()
            for k in list(sys.modules.items()): # loops through available providers to get the best rates
                if k[0].split('.')[-1].startswith('exchangerate'):
                    api = getattr(sys.modules[k[0]], "MockExchangeRate")
                    response = api().get() # api call
                    for i in response:
                        if best_values[i["code"]]>= float(i["rate"]) or best_values[i["code"]] == 0:
                            best_values[i["code"]] = float(i["rate"])
            cache.set('best_values',json.dumps(best_values),600) # sets cache
            return dict(best_values)
        else:
            cache.touch('best_values', 600)  # refresh cache timeout
            return json.loads(cache.get('best_values'))


class BestRate24h(APIView):
    """
    endpoint: /api/best_rate_last_24
    parameter: currency
    ex: http://127.0.0.1:8000/api/best_rate_last_24?currency=eur
    return: best rate last 24h

    For this one i wrote a random hourly rate generator function.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        currency = request.query_params.get('currency', None)
        if currency: # returns 404 if currency is not defined
            try:
                response = self.best_rate_last_24(currency)
                return Response({'timestamp':response['timestamp'],currency:response[currency]})
            except KeyError as e:
                return Response({"Error": "Enter a valid currency eur,usd,gbp"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"Error": "Something went so wrong " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Enter a valid currency eur,usd,gbp"}, status=status.HTTP_400_BAD_REQUEST)

    def best_rate_last_24(self,currency):

        if not cache.get('best_values_last_24_'+currency): # Checks cache
            best_values = defaultdict(int)
            for k in list(sys.modules.items()):  # loop through available providers
                if k[0].split('.')[-1].startswith('exchangerate'):
                    api = getattr(sys.modules[k[0]], "MockExchangeRate")
                    response = api().generate_random()  # api call to random hourly rate generator
                    for i in response:
                        if best_values[currency] >= float(i[currency]) or best_values[currency] == 0:
                            best_values[currency] = float(i[currency])
                            best_values['timestamp'] = i['timestamp']
            cache.set('best_values_last_24_'+currency, json.dumps(best_values), 600) # sets cache
            return best_values
        else:
            cache.touch('best_values_last_24_'+currency, 600)  # refresh cache timeout
            return json.loads(cache.get('best_values_last_24_' + currency))


