from django.urls import path

from wallets.api.v1.views import (
    ListCreateCustomerWallets, RetrieveCustomerWallets,
    CustomerWalletDepositFunds, CustomerWalletTransactions,
)

urlpatterns = [
    # List Create Customer Wallet
    path('customers/wallets', ListCreateCustomerWallets.as_view(), name='list-create-customer-wallets'),
    path('customers/wallets/<uuid>', RetrieveCustomerWallets.as_view(), name='list-create-customer-wallets'),
    path('customers/wallets/<uuid>/deposit', CustomerWalletDepositFunds.as_view(), name='customer-wallet-deposit-funds'),
    path('customers/wallets/<uuid>/transactions', CustomerWalletTransactions.as_view(), name='customer-wallet-transactions'),

    # path('/customer'),
    # # List wallet transactions
    # path('/customer/wallets/<uuid>/transactions'),
    #
    # # Business
    # # Retrieve Create Business Wallet
    # path('/business/wallet'),
    #
    # # Transactions
    # path('/business/transactions'),
]
