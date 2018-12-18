import graphene
from gapi.repository import Repository

class CloneRepo(graphene.Mutation):
    class Arguments:
        url = graphene.String()
    
    repository = graphene.Field(lambda: Repository)

    def mutate(self, info, url=None):
        # clone from github here
        # ...
        return Repository(name="test")