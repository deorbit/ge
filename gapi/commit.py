import graphene
from typing import List
import gecore.commit
import os 

class Commit(graphene.ObjectType):
    timestamp = graphene.String()
    message = graphene.String()
    author = graphene.String()
    commit_hash = graphene.String()

def get_commit_from_core(c: gecore.commit.Commit) -> Commit:
    """Convert a gecore Commit object to a GraphQL Commit object."""
    commit = Commit()
    commit.timestamp = c.timestamp
    commit.message = c.message
    commit.author = c.author
    commit.commit_hash = c.commit_hash

    return commit
    
def get_commit(repo_name: str, commit_hash:str) -> Commit:
    """Fetch a gecore Commit object using repository name and hash
    and return it as a GraphQL Commit object."""
    try:
        local_dir = os.environ['GE_REPO_DIR']
    except KeyError:
        local_dir = "./"
    local_path = os.path.join(local_dir, repo_name)
    repo = gecore.github_repo.load_repository(local_path)
    for c in repo.commits:
        if c.commit_hash == commit_hash:
            return get_commit_from_core(c)
    
def get_commits(repo_name: str) -> List[Commit]:
    """Fetch gecore commits and return them as a list of GraphQL
    commit objects."""
    try:
        local_dir = os.environ['GE_REPO_DIR']
    except KeyError:
        local_dir = "./"
    local_path = os.path.join(local_dir, repo_name)
    repo = gecore.github_repo.load_repository(local_path)
    commits = []

    for c in repo.commits:
        commits.append(get_commit_from_core(c))
        
    return commits