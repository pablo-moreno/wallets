from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.models import UserProfile

User = get_user_model()


class TestCustomers(APITestCase):
    fixtures = ('users', 'profiles', 'customer_wallets', )

    def setUp(self):
        self.user = User.objects.first()
        self.user.profile.type = UserProfile.TYPE_CUSTOMER
        self.password = 'as12345678'
        self.user.set_password(self.password)
        self.user.save()

    def login(self):
        response = self.client.post('/api/v1/users/login', {
            'username': self.user.username,
            'password': self.password,
        })
        assert response.status_code == 200

    def test_create_wallet(self):
        self.login()
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')
        response = self.client.get(f'/api/v1/wallets/customers/wallets/{uuid}')

        assert response.status_code == 200

        wallet_details = response.json()
        assert wallet_details.get('balance') == '0.00'

    def test_create_wallet_and_deposit_funds(self):
        self.login()
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')
        payload = {
            'amount': '200.00',
            'description': 'Deposit 200€',
        }

        response = self.client.patch(f'/api/v1/wallets/customers/wallets/{uuid}/deposit', payload)
        assert response.status_code == 200

        response = self.client.get(f'/api/v1/wallets/customers/wallets/{uuid}')
        assert response.status_code == 200

        wallet_details = response.json()
        assert wallet_details.get('balance') == '200.00'

        response = self.client.get(f'/api/v1/wallets/customers/wallets/{uuid}/transactions')
        assert response.status_code == 200

        transaction_list = response.json().get('results')
        assert len(transaction_list) == 1
        transaction = transaction_list[0]

        assert transaction.get('amount') == payload.get('amount')
        assert transaction.get('description') == payload.get('description')
