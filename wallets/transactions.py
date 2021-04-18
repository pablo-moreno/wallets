from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction as tr
from wallets.models import Transaction, Wallet

User = get_user_model()


class NegativeBalanceException(Exception):
    pass


def customer_deposit_into_wallet(amount: Decimal, wallet: Wallet):
    with tr.atomic():
        transaction = Transaction.objects.create(
            amount=amount,
            wallet=wallet,
            type=Transaction.TYPE_DEPOSIT,
        )

        wallet.balance += amount
        wallet.save()
        tr.status = Transaction.STATUS_ACCEPTED
        transaction.save()

    return wallet


def business_debit_transaction(transaction: Transaction):
    with tr.atomic():
        if transaction.status == Transaction.STATUS_ACCEPTED:
            return

        amount = transaction.amount
        wallet = transaction.wallet

        if amount > 0:
            amount = -amount

        wallet.balance += amount

        if wallet.balance < 0:
            transaction.status = Transaction.STATUS_REJECTED
            transaction.save()

            raise NegativeBalanceException('Balance can\'t be negative')

        wallet.save()
        transaction.status = Transaction.STATUS_ACCEPTED
