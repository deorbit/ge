import graphene
from gapi.repository import Repository
from gecore.github_repo import GitHubRepo
import os 

class CloneRepo(graphene.Mutation):
    class Arguments:
        url = graphene.String()
    
    repository = graphene.Field(lambda: Repository)

    def mutate(self, info, url=None):
        try:
            local_dir = os.environ["GE_REPO_DIR"]
        except KeyError:
            local_dir = ""
        
        repo = GitHubRepo(url=url).clone(local_dir)
        return CloneRepo(repository=Repository(
            url=url,
            name=repo.name,
            original_author=repo.original_author,
            branches=repo.branches,
            commits=repo.commits
        ))