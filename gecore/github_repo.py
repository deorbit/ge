
import git
from typing import List
from gecore.commit import Commit
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

    def clone(self: T, local_dir: str = "") -> T:
        self.name = self.url.rsplit('/', 1)[1]
        if local_dir == "":
            local_dir = self.name
        try:
            cloned_repo = git.Repo.clone_from(self.url, local_dir)
        except git.GitCommandError as err:
            print("Error cloning: {}".format(err))
            return
        self.branches = [r.name for r in cloned_repo.refs if r not in cloned_repo.tags]
        # self.commits = cloned_repo.iter_commits        
        return self