from collections import Counter

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager

from taggit.managers import TaggableManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=140, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=140, null=True)
    avatar = models.URLField(null=True)
    work_groups = models.ManyToManyField('WorkGroup')
    skills = TaggableManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']

    @property
    def latest_status(self):
        return UserStatus.objects.filter(user=self).latest('pk')


class WorkGroup(models.Model):
    name = models.CharField(max_length=140)
    created_by = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'created_by')

    @property
    def workgroup_status(self):
        statuses = WorkGroup.objects.filter(pk=self.pk)
        statuses = statuses.values('user', 'user__userstatus__status')
        statuses = statuses.order_by('-user__userstatus__created')
        status_dict = {statuses[k]['user']: statuses[k]['user__userstatus__status'] for k, v in enumerate(statuses)}
        data = Counter(status_dict.values())
        status_pk = data.most_common(1)[0][0]
        try:
            status = Status.objects.get(pk=status_pk)
            return status
        except Status.DoesNotExist:
            pass
        return None

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('web:workgroup-detail',
                       kwargs={'pk': self.pk})


class Status(models.Model):
    name = models.CharField(max_length=140, unique=True)
    priority = models.SmallIntegerField(default=1)
    css_class = models.CharField(max_length=50)
    active = models.BooleanField(default=True)


class UserStatus(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)
    description = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
