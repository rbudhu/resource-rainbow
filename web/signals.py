from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from haystack import signals

from web.models import User, UserStatus
from web.search_indexes import UserIndex


@receiver(post_save, sender=UserStatus)
def update_user_index(sender, **kwargs):
    instance = kwargs.pop('instance')
    user = instance.user
    user.save()


class UserHaystackSignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        post_save.connect(self.handle_save, sender=User)
        post_delete.connect(self.handle_delete, sender=User)

    def teardown(self):
        post_save.disconnect(self.handle_save, sender=User)
        post_delete.disconnect(self.handle_delete, sender=User)
