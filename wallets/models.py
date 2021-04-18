from decimal import Decimal
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext as _


User = get_user_model()


class TransactionStatusChoicesMixin(object):
    STATUS_PENDING = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3
    CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_REJECTED, _('Rejected'))
    )


class TransactionTypeChoicesMixin(object):
    TYPE_DEPOSIT = 1
    TYPE_DEBIT = 2
    CHOICES = (
        (TYPE_DEPOSIT, _('Deposit')),
        (TYPE_DEBIT, _('Debit')),
    )


class Transaction(models.Model, TransactionStatusChoicesMixin, TransactionTypeChoicesMixin):
    uuid = models.UUIDField(default=uuid4, db_index=True, primary_key=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250, default='', blank=True)
    status = models.PositiveIntegerField(
        choices=TransactionStatusChoicesMixin.CHOICES,
        default=TransactionStatusChoicesMixin.STATUS_PENDING,
        db_index=True,
    )
    type = models.PositiveIntegerField(
        choices=TransactionTypeChoicesMixin.CHOICES,
        default=TransactionTypeChoicesMixin.TYPE_DEBIT,
        db_index=True,
    )
    wallet = models.ForeignKey(
        'wallets.Wallet',
        on_delete=models.PROTECT,
        related_name='transactions',
        db_index=True,
        null=True,
        blank=True,
    )
    business = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_transactions',
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid4, db_index=True, primary_key=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uuid

    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class BusinessWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='business_wallet')
    wallet = models.OneToOneField(Wallet, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Business wallet')
        verbose_name_plural = _('Business wallets')


class CustomerWallets(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer_wallets')
    wallets = models.ManyToManyField(Wallet)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Customer wallets')
        verbose_name_plural = _('Customer wallets')


class BusinessCustomers(models.Model):
    business = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customers')
    customers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.business.email} customers'

    class Meta:
        verbose_name = _('Business customers')
        verbose_name_plural = _('Businesses customers')
