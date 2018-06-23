import graphene
from os import environ

from gqlapi.queries import RootQuery
from gqlapi.mutations import RootMutation

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)

# Display SQL queries on terminal if environment is DEV
if environ.get('MODE_ENVIROMENT') == 'dev':
    import logging
    from django.db import connection

    connection.force_debug_cursor = True
    logger = logging.getLogger('django.db.backends')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
