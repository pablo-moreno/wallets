from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


class TestAuthenticationMixin(object):
    def login(self, username: str, password: str):
        response = self.client.post('/api/v1/users/login', {
            'username': username,
            'password': password,
        })
        assert response.status_code == 200

    def create_account(self, username: str, password: str, account_type: int = UserProfile.TYPE_CUSTOMER):
        data = {
            'username': username,
            'email': f'{username}@example.com',
            'password': password,
            'password2': password,
            'type': UserProfile.TYPE_BUSINESS,
        }

        response = self.client.post('/api/v1/users/sign-up', data)
        return User.objects.get(username=username)
