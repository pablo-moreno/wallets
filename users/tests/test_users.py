from rest_framework.test import APITestCase
from users.models import User, UserProfile


class TestUsers(APITestCase):
    fixtures = ('users', 'profiles', )

    def setUp(self):
        self.user = User.objects.first()
        self.username = 'pablo'
        self.password = 'as12345678'
        self.user.set_password(self.password)
        self.user.save()

    def test_customer_sign_up(self):
        response = self.client.post('/api/v1/users/sign-up', {
            'username': self.username,
            'email': f'{self.username}@example.com',
            'password': self.password,
            'password2': self.password,
            'type': UserProfile.TYPE_CUSTOMER,
        })

        assert response.status_code == 201
        user = User.objects.get(username=self.username)
        assert user is not None
        assert user.profile.type == UserProfile.TYPE_CUSTOMER

    def test_business_sign_up(self):
        data = {
            'username': 'Media Market',
            'email': 'mediamarket@example.com',
            'password': self.password,
            'password2': self.password,
            'type': UserProfile.TYPE_BUSINESS,
        }

        response = self.client.post('/api/v1/users/sign-up', data)

        assert response.status_code == 201
        user = User.objects.get(email=data.get('email'))
        assert user is not None
        assert user.profile.type == UserProfile.TYPE_BUSINESS

    def test_sign_up_different_passwords(self):
        data = {
            'username': 'Media Market',
            'email': 'mediamarket@example.com',
            'password': self.password,
            'password2': 'notthesamepassword',
            'type': UserProfile.TYPE_CUSTOMER,
        }

        response = self.client.post('/api/v1/users/sign-up', data)

        assert response.status_code == 400

    def test_login(self):
        response = self.client.post('/api/v1/users/login', {
            'username': self.user.username,
            'password': self.password,
        })
        assert response.status_code == 200

    def test_wrong_login(self):
        response = self.client.post('/api/v1/users/login', {
            'username': 'notexists',
            'password': self.password,
        })
        assert response.status_code == 400

    def test_logout(self):
        response = self.client.post('/api/v1/users/login', {
            'username': self.user.username,
            'password': self.password,
        })
        assert response.status_code == 200

        response = self.client.post('/api/v1/users/logout')
        assert response.status_code == 204

    def test_login_get_me(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }

        response = self.client.post('/api/v1/users/login', data)
        assert response.status_code == 200
        response = self.client.get('/api/v1/users/me')
        assert response.status_code == 200
        user_details = response.json()

        assert self.user.username == user_details.get('username')

    def test_change_password(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }

        response = self.client.post('/api/v1/users/login', data)
        assert response.status_code == 200
        response = self.client.patch('/api/v1/users/change-password', {
            'old_password': self.password,
            'new_password': self.password[::-1],
            'new_password2': self.password[::-1],
        })
        assert response.status_code == 200

        response = self.client.post('/api/v1/users/logout')
        assert response.status_code == 204

        response = self.client.post('/api/v1/users/login', {
            'username': self.user.username,
            'password': self.password[::-1]
        })
        assert response.status_code == 200

    def test_change_password_wrong_old_password(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }

        response = self.client.post('/api/v1/users/login', data)
        assert response.status_code == 200
        response = self.client.patch('/api/v1/users/change-password', {
            'old_password': 'notthepassword',
            'new_password': self.password[::-1],
            'new_password2': self.password[::-1],
        })
        assert response.status_code == 400

    def test_delete_account(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }

        response = self.client.post('/api/v1/users/login', data)
        assert response.status_code == 200
        response = self.client.post('/api/v1/users/delete-account', data)
        self.user.refresh_from_db()
        assert self.user.is_active is False
