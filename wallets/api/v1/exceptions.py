from rest_framework.exceptions import APIException
from django.utils.translation import gettext as _


class NegativeBalanceAPIException(APIException):
    status_code = 409
    default_detail = _('Balance can\'t be negative')


class TransactionAlreadyProcessedAPIException(APIException):
    status_code = 409
    default_detail = _('Transaction already processed')
