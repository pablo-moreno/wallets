from rest_framework import serializers
from wallets.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'uuid',
            'amount',
            'description',
            'status',
            'type',
            'business',
        )
        read_only_fields = (
            'uuid',
            'status',
        )
