from django.urls import path
from .views import *

app_name = 'users'


urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='login'),
    path('sign-up', SignUp.as_view(), name='sign-up'),
    path('me', RetrieveUpdateMe.as_view(), name='me'),
    path('change-password', ChangePassword.as_view(), name='change-password'),
    path('delete-account', DeleteAccount.as_view(), name='delete-account'),
]
