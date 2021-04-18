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


class DepositWalletFundsSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=11, decimal_places=2, write_only=True)
    description = serializers.CharField(max_length=250)

    class Meta:
        model = Wallet
        fields = (
            'uuid',
            'amount',
            'description',
            'balance',
            'created_date',
            'created_date',
        )
        read_only_fields = (
            'uuid',
            'balance',
            'created_date',
            'created_date',
        )


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
