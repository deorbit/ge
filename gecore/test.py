import unittest
from gecore.github_repo import GitHubRepo, load_repository
import gecore.commit
import os
import shutil

class GeCoreTests(unittest.TestCase):
    def setUp(self):
        self.local_dest = "./test_repos/"
        try:
            os.mkdir(self.local_dest)
        except FileExistsError:
            shutil.rmtree(self.local_dest)
            os.mkdir(self.local_dest)

    def tearDown(self):
        if os.path.exists(self.local_dest):
            shutil.rmtree(self.local_dest)

    def test_normal_clone(self):
        url = "https://github.com/scanlime/zenphoton"
        repo = GitHubRepo(url).clone(local_dir = self.local_dest)
        self.assertEqual(len(repo.name), 9)
        self.assertIn("origin/multi-tool", repo.branches)
        self.assertEqual(len(repo.commits), 247)

        url = "https://github.com/requests/requests"
        repo = GitHubRepo(url).clone(local_dir = self.local_dest)
        self.assertEqual(len(repo.name), 8)
        self.assertEqual(repo.original_author, "Kenneth Reitz <me@kennethreitz.com>")

    def test_not_a_remote_repo(self):
        url = "https://github.com/deorbit"
        repo = GitHubRepo(url).clone(self.local_dest)
        self.assertEqual(len(repo.name), 0)

    def test_github_dislikes_name(self):
        """This is not a good test and I'm including it primarily
        for entertainment purposes and to show that I think about these things. 
        This is a real repository that exists but is uncloneable. The outcome of
        the test depends on GitHub's specification of "good" and "bad", which
        we have no control over. It's interesting to consider because even if it 
        could be cloned, it could conceivably cause path length issues on certain 
        operating systems."""
        url = "https://github.com/eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee/eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.git"
        repo = GitHubRepo(url).clone(self.local_dest)
        self.assertEqual(len(repo.name), 0)

    def test_clone_into_bad_dest(self):
        url = "https://github.com/hannorein/rebound.git"
        repo = GitHubRepo(url)
        repo.clone(local_dir="/well/theres/a/golden/age/coming/round")
        self.assertEqual(len(repo.name), 0)
        self.assertListEqual(repo.commits, [])

    def test_load_repository(self):
        repo = load_repository("./")
        self.assertIn("test01", repo.branches)
        self.assertEqual("ge", repo.name)

    def test_commit_timestamp(self):
        url = "https://github.com/requests/requests"
        _ = GitHubRepo(url).clone(local_dir = self.local_dest)
        commit = gecore.commit.get_commit("requests", "8761e9736f7d5508a5547cdf3adecbe0b7306278")
        self.assertEqual(commit.timestamp, "Tue, 04 Dec 2018 19:16 UTC")