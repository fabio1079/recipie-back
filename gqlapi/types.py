from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType

from culinary.models import Recipe

UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        only_fields = ("id", "email", 'is_staff', 'recipes')


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
