from .api import ExchangeRate, BestRate, BestRate24h
from rest_framework.routers import DefaultRouter
from django.urls import include, path
router = DefaultRouter(trailing_slash=False)


urlpatterns = (
    path('exchange_rate', ExchangeRate.as_view(), name='register_user'),
    path('best_rate', BestRate.as_view(), name='register_user'),
    path('best_rate_last_24', BestRate24h.as_view(), name='register_user'),
)