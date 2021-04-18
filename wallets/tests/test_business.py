from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.models import UserProfile
from .utils import TestAuthenticationMixin

User = get_user_model()


class TestBusiness(APITestCase, TestAuthenticationMixin):
    def setUp(self):
        self.username = 'mediamarket'
        self.password = 'as12345678'
        self.business = self.create_account(self.username, self.password, account_type=UserProfile.TYPE_BUSINESS)

    def test_create_retrieve_business_wallet(self):
        self.login(username=self.username, password=self.password)
        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        response = self.client.get('/api/v1/wallets/business/wallet')
        assert response.status_code == 200

        data = response.json()
        print(data)
        assert data.get('balance') == '0.00'
