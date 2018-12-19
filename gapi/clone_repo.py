import graphene
from gapi.repository import Repository
from gecore.github_repo import GitHubRepo

class CloneRepo(graphene.Mutation):
    class Arguments:
        url = graphene.String()
    
    repository = graphene.Field(lambda: Repository)

    def mutate(self, info, url=None):
        # clone from github here
        repo = GitHubRepo(url=url)
        return CloneRepo(repository=Repository(name=repo.name))