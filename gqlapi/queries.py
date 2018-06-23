import graphene

from graphql_jwt.decorators import login_required

from gqlapi.types import UserType, UserModel, Recipe, RecipeType


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(
        UserType,
        id=graphene.Int(),
        email=graphene.String())
    users = graphene.List(UserType)

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
        return UserModel.objects.all()


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

        raise Exception("User id or user email are needed")


class RootQuery(UserQuery, RecipeQuery):
    pass
