import graphene

from gqlapi.queries import RootQuery
from gqlapi.mutations import RootMutation

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
