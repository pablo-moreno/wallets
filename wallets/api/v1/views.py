from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from wallets.api.v1.serializers import WalletSerializer


class ListCreateCustomerWallets(ListCreateAPIView):
    serializer_class = WalletSerializer
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        user.customer_wallets.wallets.add(instance)
        return instance

    def get_queryset(self):
        user = self.request.user
        return user.customer_wallets.wallets.all()


class RetrieveCustomerWallets(RetrieveAPIView):
    serializer_class = WalletSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user
        return user.customer_wallets.wallets.all()
