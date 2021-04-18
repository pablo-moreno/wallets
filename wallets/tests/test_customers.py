from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.models import UserProfile
from .utils import TestAuthenticationMixin

User = get_user_model()


class TestCustomers(APITestCase, TestAuthenticationMixin):
    fixtures = ('users', 'profiles', 'customer_wallets', )

    def setUp(self):
        self.user = User.objects.first()
        self.user.profile.type = UserProfile.TYPE_CUSTOMER
        self.password = 'as12345678'
        self.user.set_password(self.password)
        self.user.save()
        self.business = self.create_account(
            username='mediamarket',
            password='mediamarket',
            account_type=UserProfile.TYPE_BUSINESS
        )

    def login(self, username, password):
        response = self.client.post('/api/v1/users/login', {
            'username': username,
            'password': password,
        })
        assert response.status_code == 200

    def test_create_wallet(self):
        self.login(username=self.user.username, password=self.password)
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')
        response = self.client.get(f'/api/v1/wallets/customers/wallets/{uuid}')

        assert response.status_code == 200

        wallet_details = response.json()
        assert wallet_details.get('balance') == '0.00'

    def test_create_wallet_and_deposit_funds(self):
        self.login(username=self.user.username, password=self.password)
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

    def test_create_wallet_deposit_and_retire_funds(self):
        self.login(username=self.user.username, password=self.password)
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')

        response = self.client.patch(f'/api/v1/wallets/customers/wallets/{uuid}/deposit', {
            'amount': '200.00',
            'description': 'Deposit 200€',
        })
        assert response.status_code == 200

        response = self.client.patch(f'/api/v1/wallets/customers/wallets/{uuid}/retire', {
            'amount': '-150.00',
            'description': 'Retire 150€',
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/v1/wallets/customers/wallets/{uuid}')
        assert response.status_code == 200

        data = response.json()
        assert data.get('balance') == '50.00'

    def test_create_wallet_deposit_and_retire_more_funds_than_you_have(self):
        self.login(username=self.user.username, password=self.password)
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')

        response = self.client.patch(f'/api/v1/wallets/customers/wallets/{uuid}/retire', {
            'amount': '-150.00',
            'description': 'Retire 150€',
        })
        assert response.status_code == 409

    def test_create_wallet_deposit_and_retire_positive_amount(self):
        self.login(username=self.user.username, password=self.password)
        response = self.client.post('/api/v1/wallets/customers/wallets')
        assert response.status_code == 201

        data = response.json()
        uuid = data.get('uuid')

        response = self.client.patch(f'/api/v1/wallets/customers/wallets/{uuid}/retire', {
            'amount': '50.00',
            'description': 'Retire 150€',
        })
        assert response.status_code == 400

    def test_create_transaction(self):
        self.login(username=self.user.username, password=self.password)

        data = {
            'amount': '1500.00',
            'description': 'TV LG OLED 55" 4K'
        }
        response = self.client.post(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions', data)
        assert response.status_code == 201

        self.client.logout()
        self.login(username=self.business.username, password=self.business.username)

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 200

        results = response.json().get('results')
        assert len(results) == 1

    def test_cannot_list_business_transaction_as_customer(self):
        self.login(username=self.user.username, password=self.password)

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 403
