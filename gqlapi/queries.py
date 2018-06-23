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
        if not info.context.user.is_staff:
            raise Exception(
                "You do not have permission to perform this action")

        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return UserModel.objects.get(pk=id)

        if email is not None:
            return UserModel.objects.get(email=email)

        raise Exception("User matching query does not exist.")

    @login_required
    def resolve_users(self, info, **kwargs):
        if info.context.user.is_staff:
            return UserModel.objects.all()
        else:
            raise Exception(
                "You do not have permission to perform this action")


class RootQuery(UserQuery):
    pass
