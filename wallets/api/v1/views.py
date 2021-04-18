from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response

from wallets.api.v1.serializers import WalletSerializer, DepositWalletFundsSerializer, TransactionSerializer
from wallets.models import Wallet, Transaction
from wallets.transactions import customer_deposit_into_wallet


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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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


class CustomerWalletTransactions(ListAPIView):
    serializer_class = TransactionSerializer

    def get_wallet(self):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(Wallet, uuid=uuid)

    def get_queryset(self):
        wallet = self.get_wallet()
        return Transaction.objects.filter(wallet=wallet)
