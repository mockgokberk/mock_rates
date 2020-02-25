from . import models
from django.contrib.auth.models import Group, User

from rest_framework import serializers


class ExchangeRateSerializer(serializers.Serializer):
    timeslot = serializers.DateTimeField()
    usd = serializers.FloatField()
    eur = serializers.FloatField()
    dbp = serializers.FloatField()
