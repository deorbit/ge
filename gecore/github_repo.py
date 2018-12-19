
import git
from typing import List
from gecore.commit import Commit
import os
import urllib
from typing import TypeVar, List

T = TypeVar('T', bound='GitHubRepo')

class GitHubRepo:
    def __init__(self, url: str = None) -> None:
        self.url = url
        self.name: str = ""
        self.original_author: str = ""
        self.branches: List[str] = []
        self.commits: List[Commit] = []

    def clone(self: T, local_dir: str = os.environ['GE_REPO_DIR']) -> T:
        try:
            cloned_repo = git.Repo.clone_from(self.url, local_dir)
        except git.GitCommandError as err:
            print("Error cloning: {}".format(err))
            return
        self.name = self.url.rsplit('/', 1)[1]
        return cloned_repo