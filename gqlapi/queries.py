import graphene

from graphql_jwt.decorators import login_required

from gqlapi.types import UserType, UserModel


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


class RootQuery(UserQuery):
    pass
