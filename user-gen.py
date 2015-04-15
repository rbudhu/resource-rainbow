from random import randrange

import requests

from web.models import User, Status, UserStatus

import django
django.setup()

skills = ['python', 'django', 'full stack', 'c++',
          'java', 'program manager', 'systems engineering',
          'configuration management', 'test engineer',
          'go', 'fortran', 'remote sensing', 'physics',
          'electro-optical imaging']

for i in range(0, 10):
    response = requests.get('http://api.randomuser.me/')
    response = response.json()
    person = response['results'][0]['user']
    first_name = person['name']['first']
    last_name = person['name']['last']
    username = person['username']
    password = person['password']
    email = person['email']
    phone_number = person['phone']
    location = '{}, {}'.format(person['location']['city'],
                               person['location']['state'])
    avatar = person['picture']['thumbnail']
    user = User.objects.create(username=username,
                               first_name=first_name.title(),
                               last_name=last_name.title(),
                               email=email,
                               password=password,
                               phone_number=phone_number,
                               location=location.title(),
                               avatar=avatar)
    
    skill_index = randrange(0, len(skills))
    for skill in skills[skill_index:skill_index+3]:
        user.skills.add(skill)
    status = Status.objects.get(pk=randrange(1,4))
    user_status = UserStatus.objects.create(user=user, status=status)
