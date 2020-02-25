from django.test import TestCase
from .wrappers import exchangerate_mock1
from .wrappers import exchangerate_mock2
from .wrappers import exchangerate_mock3
from rest_framework.test import APIClient

class TestWrappers(TestCase):
    """
    Api wrappers tests
    """
    def setUp(self):
        pass

    def test_request(self):
        response = exchangerate_mock1.MockExchangeRate().get(serialize=False)
        self.assertEqual(response.status_code, 200)

    def test_request_value(self):
        r = exchangerate_mock1.MockExchangeRate().get()
        self.assertIsInstance(r, list)
        self.assertEqual(r[0]["code"], 'usd')

    def test_request2(self):
        response = exchangerate_mock2.MockExchangeRate().get(serialize=False)
        self.assertEqual(response.status_code, 200)

    def test_request2_value(self):
        r = exchangerate_mock2.MockExchangeRate().get()
        self.assertIsInstance(r, list)
        self.assertEqual(r[0]["code"], 'usd')

    def test_request3(self):
        response = exchangerate_mock3.MockExchangeRate().get(serialize=False)
        self.assertEqual(response.status_code, 200)

    def test_request3_value(self):
        r = exchangerate_mock3.MockExchangeRate().get()
        self.assertIsInstance(r, list)
        self.assertEqual(r[0]["code"], 'usd')

    def test_random_values(self):
        r = exchangerate_mock1.MockExchangeRate().generate_random()
        self.assertIsInstance(r, list)

    def test_random_values2(self):
        r = exchangerate_mock2.MockExchangeRate().generate_random()
        self.assertIsInstance(r, list)

    def test_random_values3(self):
        r = exchangerate_mock3.MockExchangeRate().generate_random()
        self.assertIsInstance(r, list)


class TestDrf(TestCase):
    """
    Api endpoints tests
    """
    def setUp(self):
        self.factory = APIClient()

    def test_drf_prices(self):
        response = self.factory.get('/api/exchange_rate?provider=exchangerate_mock1')
        self.assertEqual(response.status_code, 200)

    def test_drf_prices2(self):
        response = self.factory.get('/api/exchange_rate?provider=exchangerate_mock1')
        self.assertEqual(response.status_code, 200)

    def test_drf_prices3(self):
        response = self.factory.get('/api/exchange_rate?provider=exchangerate_mock3')
        self.assertEqual(response.status_code, 200)

    def test_invalid_provider(self):
        response = self.factory.get('/api/exchange_rate')
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'Error': 'No provider specified'})

    def test_best_rate(self):
        response = self.factory.get('/api/best_rate')
        self.assertEqual(response.status_code, 200)

    def test_best_rate_error(self):
        response = self.factory.get('/api/best_rate?currency=try')
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"Error":"Enter a valid currency eur,usd,gbp"})

    def test_best_rate_value(self):
        response = self.factory.get('/api/best_rate')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('usd', response.json())
        self.assertIn('gbp', response.json())
        self.assertIn('eur', response.json())

    def test_best_rate_eur(self):
        response = self.factory.get('/api/best_rate?currency=eur')
        self.assertEqual(response.status_code, 200)

    def test_best_rate_eur_value(self):
        response = self.factory.get('/api/best_rate?currency=eur')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('eur', response.json())

    def test_best_rate_usd(self):
        response = self.factory.get('/api/best_rate?currency=usd')
        self.assertEqual(response.status_code, 200)

    def test_best_rate_usd_value(self):
        response = self.factory.get('/api/best_rate?currency=usd')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('usd', response.json())

    def test_best_rate_gbp(self):
        response = self.factory.get('/api/best_rate?currency=gbp')
        self.assertEqual(response.status_code, 200)

    def test_best_rate_gbp_value(self):
        response = self.factory.get('/api/best_rate?currency=gbp')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('gbp', response.json())

    def test_best_rate_last_24(self):
        response = self.factory.get('/api/best_rate_last_24?currency=eur')
        self.assertEqual(response.status_code, 200)

    def test_best_rate_last_24_value_eur(self):
        response = self.factory.get('/api/best_rate_last_24?currency=eur')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('eur', response.json())

    def test_best_rate_last_24_value_gbp(self):
        response = self.factory.get('/api/best_rate_last_24?currency=gbp')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('gbp', response.json())

    def test_best_rate_last_24_value_usd(self):
        response = self.factory.get('/api/best_rate_last_24?currency=usd')
        self.assertIsInstance(response.json(), dict)
        self.assertIn('usd', response.json())