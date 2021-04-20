from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction as tr
from wallets.models import Transaction, Wallet

User = get_user_model()


class NegativeBalanceException(Exception):
    pass


class TransactionAlreadyProcessedException(Exception):
    pass


def customer_deposit_into_wallet(amount: Decimal, wallet_id: int, customer: User, description: str = '') -> Wallet:
    """
        Customer deposits funds into a wallet

        :param amount: Amount to deposit into the wallet
        :param wallet_id: Wallet ID
        :param customer: Customer's user
        :param description: Description of the transaction

    """
    with tr.atomic():
        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)

        transaction = Transaction.objects.create(
            amount=amount,
            wallet=wallet,
            type=Transaction.TYPE_DEPOSIT,
            customer=customer,
            description=description,
        )

        wallet.balance += amount
        wallet.save()
        tr.status = Transaction.STATUS_ACCEPTED
        transaction.save()

    return wallet


def customer_retire_funds_from_wallet(amount: Decimal, wallet_id: int, customer: User, description: str = '') -> Wallet:
    """
        Customer retires atomically funds from a specified wallet

        :param amount: Amount to retire
        :param wallet_id: Wallet ID
        :param customer: Customer's user
        :param description: Description of the transaction

        :raises NegativeBalanceException:
    """

    with tr.atomic():
        amount = abs(amount)

        wallet = Wallet.objects.select_for_update().get(pk=wallet_id)

        if wallet.balance - amount < 0:
            raise NegativeBalanceException('Balance can\'t be negative')

        transaction = Transaction.objects.create(
            amount=-amount,
            wallet=wallet,
            type=Transaction.TYPE_DEBIT,
            customer=customer,
            description=description,
        )

        wallet.balance -= amount
        wallet.save()
        transaction.status = Transaction.STATUS_ACCEPTED
        transaction.save()

    return wallet


def business_debit_transaction(transaction_id: int) -> Transaction:
    """
        Debit customer transaction

        :param transaction_id: Transaction ID

        :raises NegativeBalanceException:
        :raises TransactionAlreadyProcessedException:
    """
    with tr.atomic():
        transaction = Transaction.objects.select_for_update().get(pk=transaction_id)
        business = transaction.business

        if transaction.status == Transaction.STATUS_ACCEPTED:
            raise TransactionAlreadyProcessedException('Can\'t debit an already accepted transaction.')

        amount = abs(transaction.amount)
        wallet = Wallet.objects.select_for_update().get(pk=transaction.wallet_id)

        wallet.balance -= amount
        business_wallet = Wallet.objects.select_for_update().get(pk=business.business_wallet.wallet_id)
        business_wallet.balance += amount

        if wallet.balance < 0:
            transaction.status = Transaction.STATUS_REJECTED
            transaction.save()

            raise NegativeBalanceException('Balance can\'t be negative')

        wallet.save()
        business_wallet.save()
        transaction.status = Transaction.STATUS_ACCEPTED
        transaction.save()

    return transaction
