import graphene
from gapi.clone_repo import CloneRepo

class GiMutations(graphene.ObjectType):
    """Root mutation."""
    clone_repo = CloneRepo.Field()