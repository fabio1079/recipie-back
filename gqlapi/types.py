from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType

UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ("id", "email", 'is_staff',)
