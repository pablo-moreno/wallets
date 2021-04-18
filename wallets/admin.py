from django.contrib import admin
from wallets.models import (
    Transaction, Wallet,  CustomerWallets, BusinessWallet
)

admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(CustomerWallets)
admin.site.register(BusinessWallet)
