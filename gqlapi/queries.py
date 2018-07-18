import graphene

from graphql_jwt.decorators import login_required

from culinary.models import Recipe, RecipeDifficultyChoices
from gqlapi.types import (
    UserType, UserModel, RecipeType, RecipeDifficultyType)


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(
        UserType,
        id=graphene.Int(),
        email=graphene.String())

    users = graphene.List(UserType,
        first=graphene.Int(),
        skip=graphene.Int())

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return UserModel.objects.get(pk=id)

        if email is not None:
            return UserModel.objects.get(email=email)

        raise Exception("User matching query does not exist.")

    @login_required
    def resolve_users(self, info, **kwargs):
        first = kwargs.get('first', 10)
        skip = kwargs.get('skip')

        qs = UserModel.objects.all()

        if skip:
            qs = qs[skip::]

        if first:
            qs = qs[:first]

        return qs


class RecipeQuery(graphene.ObjectType):
    recipes = graphene.List(
        RecipeType,
        user_id=graphene.ID(),
        user_email=graphene.String())

    def resolve_recipes(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        user_email = kwargs.get('user_email')
        query = Recipe.objects.all().select_related('user')

        if user_id is not None:
            return query.filter(user=user_id)

        if user_email is not None:
            return query.filter(user__email=user_email)

        return query


class RecipeDifficultyQuery(graphene.ObjectType):
    difficulties = graphene.List(RecipeDifficultyType)

    def resolve_difficulties(self, info, **kwargs):
        return [
            RecipeDifficultyType(name=d.name, value=d.value)
            for d in RecipeDifficultyChoices
        ]


class RootQuery(UserQuery, RecipeQuery, RecipeDifficultyQuery):
    pass
