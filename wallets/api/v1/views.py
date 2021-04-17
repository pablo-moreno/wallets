from rest_framework.generics import ListCreateAPIView

from users.models import UserProfile
from wallets.api.v1.serializers import TransactionSerializer
from wallets.models import Transaction


class ListCreateTransaction(ListCreateAPIView):
    serializer_class = TransactionSerializer
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.profile.type == UserProfile.TYPE_BUSINESS:
            return Transaction.objects.filter(business=user)

        return Transaction.objects.filter(user=user)

