
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
    """GitHubRepo represents a git repository fetched from
    a remote source or loaded into memory from the local disk.

    Attributes:
        url: source URL
        name: local name of the repository
        original_author: who wrote the first commit?
        branches: list of branches
        commits: list of all commits
    """
    def __init__(self, url: str = None) -> None:
        self.url = url
        self.name: str = ""
        self.original_author: str = ""
        self.branches: List[str] = []
        self.commits: List[gecore.commit.Commit] = []

    def clone(self: T, local_dir: str = "") -> T:
        """Clones a git repository hosted at self.url into local_dir.
        Args:
            local_dir: directory holding the .git directory

        Returns:
            A GitHubRepo object representing the repository.
        """
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
        format for in-memory use.

        Args:
            repo: a repository object produced by the GitPython package

        Returns:
            A GitHubRepo object representing the repository.
        """
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
    """Load a repository from disk into memory.
    
    Args:
        repo_dir: name of directory containing the .git directory

    Returns:
        A GitHubRepo representing the repository loaded from disk
    """
    return GitHubRepo.from_GitPython(git.Repo(repo_dir))
