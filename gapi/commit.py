import graphene
from typing import List
import gecore.commit
import os 

class Commit(graphene.ObjectType):
    timestamp = graphene.String()
    message = graphene.String()
    author = graphene.String()
    commit_hash = graphene.String()

def get_commit(c: gecore.commit.Commit) -> Commit:
    commit = Commit()
    commit.timestamp = c.timestamp
    commit.message = c.message
    commit.author = c.author
    commit.commit_hash = c.commit_hash

    return commit
    
def get_commits(repo_name: str) -> List[Commit]:
    try:
        local_dir = os.environ['GE_REPO_DIR']
    except KeyError:
        local_dir = "./"
    local_path = os.path.join(local_dir, repo_name)
    repo = gecore.github_repo.load_repository(local_path)
    commits = []

    for c in repo.commits:
        commits.append(get_commit(c))
        
    return commits