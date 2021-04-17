from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import models
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
    uuid = models.UUIDField(default=uuid4, db_index=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    status = models.PositiveIntegerField(choices=TransactionStatusChoicesMixin.CHOICES, db_index=True)
    type = models.PositiveIntegerField(choices=TransactionTypeChoicesMixin.CHOICES, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid4, db_index=True)
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
