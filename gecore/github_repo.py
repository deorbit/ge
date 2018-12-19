
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
        if not name.endswith(".git"):
            return GitHubRepo()
        if local_dir == "":
            local_dir = name
        try:
            cloned_repo = git.Repo.clone_from(self.url, local_dir)
        except git.GitCommandError as err:
            print("Error cloning: {}".format(err))
            return GitHubRepo()
        self.name = name
        self.branches = [r.name for r in cloned_repo.refs if r not in cloned_repo.tags]
        self.commits = [Commit(
                    commit_hash = c.hexsha,
                    timestamp = str(time.gmtime(c.committed_date)),
                    message = c.message,
                    author = str(c.author))
                for c in cloned_repo.iter_commits()]
        return self