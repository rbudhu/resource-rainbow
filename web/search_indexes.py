from haystack import indexes

from web.models import User, UserStatus

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    status = indexes.IntegerField(null=True)

    def get_model(self):
        return User

    def prepare_status(self, obj):
        try:
            user_status = UserStatus.objects.filter(user=obj).latest('pk')
            return user_status.status.pk
        except UserStatus.DoesNotExist:
            return None
        
