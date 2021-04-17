from uuid import uuid1
from django.core.management.base import BaseCommand
import requests
from users.models import UserProfile, User


class Command(BaseCommand):
    help = 'Generate users using randomuser.me API'

    def fetch_users(self):
        results = []

        params = {'nat': 'es', 'results': 100}
        response = requests.get('https://randomuser.me/api/', params)
        request_results = response.json()['results']

        for user in request_results:
            uid = str(uuid1()).split('-')[-1]
            results.append({
                'first_name': user['name']['first'],
                'last_name': user['name']['last'],
                'email': f"{uid}.{user['email']}",
                'username': user['login']['username'],
            })

        return results

    def handle(self, *args, **options):
        results = self.fetch_users()

        for user in results:
            u = User.objects.create(**user)
            u.set_password('as12345678')
            u.save()

            UserProfile.objects.create(
                user=u,
                type=UserProfile.TYPE_CUSTOMER,
            )
