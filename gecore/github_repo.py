
import git
from typing import List
from gecore.commit import Commit
from urllib.parse import urlparse
from typing import TypeVar, List
import base64
import time
import os 

T = TypeVar('T', bound='GitHubRepo')

class GitHubRepo:
    def __init__(self, url: str = None) -> None:
        self.url = url
        self.name: str = ""
        self.original_author: str = ""
        self.branches: List[str] = []
        self.commits: List[Commit] = []

    def clone(self: T, local_dir: str = "") -> T:
        """Clones a git repository hosted at self.url into local_dir."""
        name = os.path.basename(urlparse(self.url).path)
        if local_dir == "":
            local_dir = name
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
        r.commits = [Commit(
                    commit_hash = c.hexsha,
                    timestamp = str(time.gmtime(c.committed_date)),
                    message = c.message,
                    author = str(c.author))
                for c in repo.iter_commits()]
        return r

def load_repository(name: str, local_dir: str) -> GitHubRepo:
    """Load a repository from disk into memory."""
    return GitHubRepo.from_GitPython(git.Repo(os.path.join(local_dir, name)))
