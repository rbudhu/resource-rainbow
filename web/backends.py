import re
import json
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

from web.models import User


class JiveBackend(object):

    def authenticate(self, username=None, password=None):
        auth = HTTPBasicAuth(username, password)
        jive_api_url = settings.JIVE_API_URL
        url = '{}/people/username/{}'.format(jive_api_url, username)
        response = requests.get(url, auth=auth)
        if response.status_code != 200:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            person = response.text
            person = re.sub('^throw.*;\\s*', '', person)
            try:
                person = json.loads(person)
                print(json.dumps(person, indent=2))
                email, location, phone_number = None, None, None
                last_name = person['name']['familyName']
                first_name = person['name']['givenName']
                avatar = person['thumbnailUrl']
                emails = person['emails']
                addresses = person['addresses']
                phone_numbers = person['phoneNumbers']
                for eml in emails:
                    if eml['type'] == 'work':
                        email = eml['value']
                        break
                if email is None:
                    return None
                for address in addresses:
                    city = address['value']['locality']
                    state = address['value']['region']
                    location = '{}, {}'.format(city, state)
                    break
                for phone in phone_numbers:
                    if phone['type'] == 'work':
                        phone_number = phone['value']
                        break
                user = User()
                user.last_name = last_name
                user.first_name = first_name
                user.email = email
                user.phone_number = phone_number
                user.location = location
                user.avatar = avatar
                user.username = username
                user.set_password(password)
                user.save()
                return user
            except (KeyError, ValueError):
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
