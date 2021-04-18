from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from wallets.api.v1.serializers import WalletSerializer, DepositWalletFundsSerializer
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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        amount = data.get('amount')
        wallet = customer_deposit_into_wallet(wallet=instance, amount=amount)
        response_data = WalletSerializer(wallet).data

        return Response(data=response_data, status=status.HTTP_200_OK)
