from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserProfile(models.Model):
    TYPE_CUSTOMER = 1
    TYPE_BUSINESS = 2
    TYPE_CHOICES = (
        (TYPE_CUSTOMER, _('Customer')),
        (TYPE_BUSINESS, _('Business')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=TYPE_CUSTOMER, db_index=True)

    def __str__(self):
        return f'{self.user.email}'
