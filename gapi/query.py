import graphene
from gapi.repository import Repository

class GiQuery(graphene.ObjectType):
    """The root query for the GraphQL service."""
    repository = graphene.Field(Repository)
    # commit = 
