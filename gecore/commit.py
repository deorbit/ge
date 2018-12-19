class Commit:
    def __init__(self, timestamp = "", message = "", author = "", commit_hash = ""):
        self.timestamp: str = timestamp
        self.message: str = message
        self.author: str = author
        self.commit_hash: str = commit_hash