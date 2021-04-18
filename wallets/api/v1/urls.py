from django.urls import path

from wallets.api.v1.views import (
    ListCreateCustomerWallets, RetrieveCustomerWallets,
    CustomerWalletDepositFunds, CustomerWalletTransactions, RetrieveCreateBusinessWallet, CustomerWalletRetireFunds,
    ListCreateTransaction, DebitTransaction,
)

urlpatterns = [
    # Customers
    path('customers/wallets', ListCreateCustomerWallets.as_view(), name='list-create-customer-wallets'),
    path('customers/wallets/<uuid>', RetrieveCustomerWallets.as_view(), name='list-create-customer-wallets'),
    path('customers/wallets/<uuid>/deposit', CustomerWalletDepositFunds.as_view(), name='customer-wallet-deposit-funds'),
    path('customers/wallets/<uuid>/retire', CustomerWalletRetireFunds.as_view(), name='customer-wallet-retire-funds'),
    path('customers/wallets/<uuid>/transactions', CustomerWalletTransactions.as_view(), name='customer-wallet-transactions'),

    # Business
    path('business/wallet', RetrieveCreateBusinessWallet.as_view(), name='retrieve-create-business-wallet'),
    path('business/<id>/customers/transactions', ListCreateTransaction.as_view(), name='list-create-transaction'),
    path('business/transactions/<uuid>/debit', DebitTransaction.as_view(), name='debit-transaction'),
]
