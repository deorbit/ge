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