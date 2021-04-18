from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, get_object_or_404, \
    CreateAPIView
from rest_framework.response import Response
from django.utils.translation import gettext as _

from wallets.api.v1.exceptions import NegativeBalanceAPIException
from wallets.api.v1.serializers import WalletSerializer, DepositWalletFundsSerializer, TransactionSerializer, \
    RetireWalletFundsSerializer
from wallets.models import Wallet, Transaction
from wallets.transactions import customer_deposit_into_wallet, customer_retire_funds_from_wallet, \
    NegativeBalanceException


class CustomerWalletsQuerysetMixin(object):
    def get_queryset(self):
        user = self.request.user
        return user.customer_wallets.wallets.all()


class ListCreateCustomerWallets(CustomerWalletsQuerysetMixin, ListCreateAPIView):
    serializer_class = WalletSerializer
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        user.customer_wallets.wallets.add(instance)
        return instance


class RetrieveCustomerWallets(CustomerWalletsQuerysetMixin, RetrieveAPIView):
    serializer_class = WalletSerializer
    lookup_field = 'uuid'


class CustomerWalletDepositFunds(CustomerWalletsQuerysetMixin, UpdateAPIView):
    serializer_class = DepositWalletFundsSerializer
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        amount = data.get('amount')
        description = data.get('description')
        wallet = customer_deposit_into_wallet(
            wallet=instance,
            amount=amount,
            customer=user,
            description=description
        )
        response_data = WalletSerializer(wallet).data

        return Response(data=response_data, status=status.HTTP_200_OK)


class CustomerWalletRetireFunds(CustomerWalletsQuerysetMixin, UpdateAPIView):
    serializer_class = RetireWalletFundsSerializer
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        amount = data.get('amount')
        description = data.get('description')

        try:
            wallet = customer_retire_funds_from_wallet(
                wallet=instance,
                amount=amount,
                customer=user,
                description=description
            )
        except NegativeBalanceException as e:
            raise NegativeBalanceAPIException()

        response_data = WalletSerializer(wallet).data

        return Response(data=response_data, status=status.HTTP_200_OK)


class CustomerWalletTransactions(ListAPIView):
    serializer_class = TransactionSerializer

    def get_wallet(self):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(Wallet, uuid=uuid)

    def get_queryset(self):
        wallet = self.get_wallet()
        return Transaction.objects.filter(wallet=wallet)


class RetrieveCreateBusinessWallet(RetrieveAPIView, CreateAPIView):
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save()
        user.business_wallet.wallet = instance
        user.business_wallet.save()

    def get_object(self):
        user = self.request.user
        return user.business_wallet.wallet
