from rest_framework import serializers
from wallets.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            'uuid',
            'balance',
            'created_date',
            'created_date',
        )
        read_only_fields = fields


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
