
import git
from typing import List
import gecore.commit
from urllib.parse import urlparse
from typing import TypeVar, List
import base64
import time
import os 
from datetime import datetime

T = TypeVar('T', bound='GitHubRepo')

class GitHubRepo:
    def __init__(self, url: str = None) -> None:
        self.url = url
        self.name: str = ""
        self.original_author: str = ""
        self.branches: List[str] = []
        self.commits: List[gecore.commit.Commit] = []

    def clone(self: T, local_dir: str = "") -> T:
        """Clones a git repository hosted at self.url into local_dir."""
        name = os.path.basename(urlparse(self.url).path)
        if local_dir == "":
            local_dir = name
        else:
            local_dir = os.path.join(local_dir, name)
        try:
            cloned_repo = git.Repo.clone_from(self.url, local_dir)
        except git.GitCommandError as err:
            print("Error cloning: {}".format(err))
            return GitHubRepo()
        in_memory_repo = GitHubRepo.from_GitPython(cloned_repo)
        in_memory_repo.name = name
        return in_memory_repo

    @staticmethod
    def from_GitPython(repo: git.Repo) -> T:
        """Converts a GitPython Repo into our GitHubRepo
        format for in-memory use."""
        r = GitHubRepo()
        r.branches = [r.name for r in repo.refs if r not in repo.tags]
        r.commits = [gecore.commit.Commit(
                    commit_hash = c.hexsha,
                    timestamp = time.strftime("%a, %d %b %Y %H:%M UTC", time.gmtime(c.authored_date)),
                    message = c.message,
                    author = c.author.name + " <" + c.author.email + ">")
                for c in repo.iter_commits()]
        first_commit = r.commits[-1]
        r.original_author = first_commit.author
        r.name = os.path.split(repo.working_tree_dir)[1]
        return r

def load_repository(repo_dir: str) -> GitHubRepo:
    """Load a repository from disk into memory."""
    return GitHubRepo.from_GitPython(git.Repo(repo_dir))
