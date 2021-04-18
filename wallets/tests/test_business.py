from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.models import UserProfile
from .utils import TestAuthenticationMixin
from ..models import Transaction, Wallet

User = get_user_model()


class TestBusiness(APITestCase, TestAuthenticationMixin):
    fixtures = ('users', 'profiles', 'customer_wallets')

    def setUp(self):
        self.username = 'mediamarket'
        self.password = 'as12345678'
        self.business = self.create_account(self.username, self.password, account_type=UserProfile.TYPE_BUSINESS)
        self.other_business = self.create_account('marketmedia', 'marketmedia', account_type=UserProfile.TYPE_BUSINESS)

    def create_customer_data(self, business: User, wallet_funds: Decimal = Decimal('200.00'), transactions_number: int = 3,
                             amount: Decimal = Decimal('10.00')) -> (User, Wallet):
        customer = UserProfile.objects.filter(type=UserProfile.TYPE_CUSTOMER).first().user

        wallet = Wallet.objects.create()
        wallet.balance = wallet_funds
        wallet.save()

        customer.customer_wallets.wallets.add(wallet)

        for i in range(transactions_number):
            Transaction.objects.create(
                amount=amount,
                description=f'Transaction #{i}',
                wallet=wallet,
                business=business,
            )
        return customer, wallet

    def test_create_retrieve_business_wallet(self):
        self.login(username=self.username, password=self.password)
        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        response = self.client.get('/api/v1/wallets/business/wallet')
        assert response.status_code == 200

        data = response.json()
        assert data.get('balance') == '0.00'

    def test_list_business_transactions(self):
        self.login(username=self.username, password=self.password)
        self.create_customer_data(self.business)

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 200
        data = response.json()
        assert data.get('count') == 3

    def test_debit_transaction(self):
        self.login(username=self.username, password=self.password)

        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        business_wallet = self.business.business_wallet.wallet

        assert business_wallet.balance == Decimal('0.00')

        transaction_amount = Decimal('15.00')
        customer, wallet = self.create_customer_data(self.business, transactions_number=1, amount=transaction_amount)
        previous_balance = wallet.balance

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 200
        data = response.json()
        assert data.get('count') == 1

        results = data.get('results')
        transaction_id = results[0].get('uuid')

        response = self.client.patch(f'/api/v1/wallets/business/transactions/{transaction_id}/debit')
        assert response.status_code == 200

        wallet.refresh_from_db()
        business_wallet.refresh_from_db()
        assert wallet.balance == previous_balance - transaction_amount
        assert Transaction.objects.last().status == Transaction.STATUS_ACCEPTED
        assert business_wallet.balance == transaction_amount

    def test_debit_same_transaction_twice(self):
        self.login(username=self.username, password=self.password)

        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        business_wallet = self.business.business_wallet.wallet

        transaction_amount = Decimal('15.00')
        customer, wallet = self.create_customer_data(self.business, transactions_number=1, amount=transaction_amount)
        previous_balance = wallet.balance

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 200
        data = response.json()
        assert data.get('count') == 1

        results = data.get('results')
        transaction_id = results[0].get('uuid')

        response = self.client.patch(f'/api/v1/wallets/business/transactions/{transaction_id}/debit')
        assert response.status_code == 200

        response = self.client.patch(f'/api/v1/wallets/business/transactions/{transaction_id}/debit')
        assert response.status_code == 409

        wallet.refresh_from_db()
        business_wallet.refresh_from_db()
        assert wallet.balance == previous_balance - transaction_amount
        assert Transaction.objects.last().status == Transaction.STATUS_ACCEPTED
        assert business_wallet.balance == transaction_amount

    def test_cannot_debit_negative_balance(self):
        self.login(username=self.username, password=self.password)

        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        business_wallet = self.business.business_wallet.wallet

        transaction_amount = Decimal('15.00')
        customer, wallet = self.create_customer_data(
            self.business,
            wallet_funds=Decimal('10.00'),
            transactions_number=1,
            amount=transaction_amount
        )

        response = self.client.get(f'/api/v1/wallets/business/{self.business.pk}/customers/transactions')
        assert response.status_code == 200
        data = response.json()

        results = data.get('results')
        transaction_id = results[0].get('uuid')

        response = self.client.patch(f'/api/v1/wallets/business/transactions/{transaction_id}/debit')
        assert response.status_code == 409

        business_wallet.refresh_from_db()
        assert business_wallet.balance == Decimal('0.00')

    def test_cannot_debit_transaction_from_other_business(self):
        self.login(username=self.username, password=self.password)

        response = self.client.post('/api/v1/wallets/business/wallet')
        assert response.status_code == 201

        business_wallet = self.business.business_wallet.wallet

        transaction_amount = Decimal('15.00')
        customer, wallet = self.create_customer_data(
            self.other_business,
            wallet_funds=Decimal('200.00'),
            transactions_number=1,
            amount=transaction_amount
        )

        uuid = Transaction.objects.filter(business=self.other_business).first().uuid

        response = self.client.patch(f'/api/v1/wallets/business/transactions/{uuid}/debit')
        assert response.status_code == 404

        business_wallet.refresh_from_db()
        assert business_wallet.balance == Decimal('0.00')
