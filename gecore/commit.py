import gecore.github_repo
import os

class Commit:
    def __init__(self, 
        timestamp:str = "", 
        message:str = "", 
        author:str = "", 
        commit_hash:str = "") -> None:
        self.timestamp: str = timestamp
        self.message: str = message
        self.author: str = author
        self.commit_hash: str = commit_hash

def get_commit(repo_name: str, commit_hash:str) -> Commit:
    """Fetch a gecore Commit object using repository name and hash."""
    try:
        local_dir = os.environ['GE_REPO_DIR']
    except KeyError:
        local_dir = "./"
    local_path = os.path.join(local_dir, repo_name)
    repo = gecore.github_repo.load_repository(local_path)
    for c in repo.commits:
        if c.commit_hash == commit_hash:
            return c
    return Commit()