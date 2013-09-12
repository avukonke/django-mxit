import json

from django.test import TestCase
from django.test.client import Client


class MxitTest(TestCase):

    def test_login_required(self):
        client = Client()
        response = client.get('/')
        self.assertRedirects(
            response, '/accounts/login/?next=/', target_status_code=404)

    def test_login(self):
        client = Client()
        response = client.get('/', **{
            'HTTP_X_DEVICE_USER_AGENT': 'user-agent',
            'HTTP_X_MXIT_CONTACT': 'contact',
            'HTTP_X_MXIT_USERID_R': 'userid-r',
            'HTTP_X_MXIT_NICK': 'nick',
            'HTTP_X_MXIT_LOCATION': 'za,south africa,,,ct,cape town,,,,',
            'HTTP_X_MXIT_PROFILE': 'en,za,01-01-2013,,,',
            'HTTP_X_MXIT_USER_INPUT': '&lt;b&gt;foo&lt;/b&gt;',
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        mxit_data = data['mxit']
        username = data['username']
        self.assertEqual(username, 'userid-r')
        self.assertEqual(mxit_data['DEVICE_USER_AGENT'], 'user-agent')
        self.assertEqual(mxit_data['MXIT_CONTACT'], 'contact')
        self.assertEqual(mxit_data['MXIT_USERID_R'], 'userid-r')
        self.assertEqual(mxit_data['MXIT_NICK'], 'nick')
        self.assertEqual(mxit_data['MXIT_LOCATION'], {
            'cell_id': '',
            'city': 'cape town',
            'city_code': 'ct',
            'client_features_bitset': '',
            'country_code': 'za',
            'country_name': 'south africa',
            'network_operator_id': '',
            'subdivision_code': '',
            'subdivision_name': '',
        })
        self.assertEqual(mxit_data['MXIT_PROFILE'], {
            'country_code': 'za',
            'date_of_birth': '01-01-2013',
            'gender': '',
            'language_code': 'en',
            'tariff_plan': '',
        })
        self.assertEqual(mxit_data['MXIT_USER_INPUT'], '<b>foo</b>')
