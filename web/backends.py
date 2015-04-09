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
                email = None
                last_name = person['name']['familyName']
                first_name = person['name']['givenName']
                emails = person['emails']
                for eml in emails:
                    if eml['type'] == 'work':
                        email = eml['value']

                if email is None:
                    return None
                user = User()
                user.last_name = last_name
                user.first_name = first_name
                user.email = email
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
