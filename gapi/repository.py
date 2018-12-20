import graphene
from gapi.commit import Commit, get_commits, get_commit
import gecore.github_repo
import os

class Repository(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()
    original_author = graphene.String()
    branches = graphene.List(graphene.String)
    commits = graphene.List(Commit)

    def resolve_commits(self, info):
        return get_commits(self.name)

def get_repository(name: str = None):
    try:
        local_dir = os.environ['GE_REPO_DIR']
    except KeyError:
        local_dir = "./"
    local_path = os.path.join(local_dir, name)
    local_repo = gecore.github_repo.load_repository(local_path)
    repo = Repository()
    repo.url = local_repo.url
    repo.name = local_repo.name
    repo.original_author = local_repo.original_author
    repo.branches = local_repo.branches
    repo.commits = map(get_commit, local_repo.commits)

    return repo