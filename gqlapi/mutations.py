import graphene

from graphql_jwt import (ObtainJSONWebToken, Verify, Refresh)

from gqlapi.types import UserType, UserModel


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


class RootMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
    create_user = CreateUser.Field()
