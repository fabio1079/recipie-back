import graphene
from django.shortcuts import get_object_or_404

from graphql_jwt import (ObtainJSONWebToken, Verify, Refresh)

from gqlapi.types import UserType, UserModel, Recipe, RecipeType


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = UserModel(
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class CreateRecipe(graphene.Mutation):
    recipe = graphene.Field(RecipeType)

    class Arguments:
        user_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        time_needed = graphene.Int(required=True)
        difficulty = graphene.String(required=True)
        picture = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        name = kwargs.get('name')
        time_needed = kwargs.get('time_needed')
        picture = kwargs.get('picture')
        difficulty = kwargs.get('difficulty')

        user = get_object_or_404(UserModel, pk=user_id)

        recipe = Recipe(
            user=user,
            name=name,
            time_needed=time_needed,
            picture=picture,
            difficulty=difficulty)
        recipe.save()

        return CreateRecipe(recipe=recipe)


class RootMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
    create_user = CreateUser.Field()
    create_recipe = CreateRecipe.Field()
