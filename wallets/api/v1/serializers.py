from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from wallets.models import Transaction, Wallet


User = get_user_model()


class BusinessSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = (
            'id',
            'name'
        )


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

    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError('Amount must be positive')

        return amount

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


class RetireWalletFundsSerializer(DepositWalletFundsSerializer):
    def validate_amount(self, amount):
        if amount > 0:
            raise ValidationError('Amount must be negative')

        return amount


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
            'wallet',
        )
        read_only_fields = (
            'uuid',
            'status',
        )
