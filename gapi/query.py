import graphene
from gapi.repository import Repository, get_repository
from gapi.commit import Commit

class GiQuery(graphene.ObjectType):
    """The root query for the GraphQL service."""
    repository = graphene.Field(Repository, name=graphene.String())
    commit = graphene.Field(Commit, name=graphene.String(), hash=graphene.String())

    def resolve_repository(self, info, name=None):
        return get_repository(name)

    # def resolve_commit(self, info, name=None, hash=None):
    #     return get
