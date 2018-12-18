import graphene

class Commit(graphene.ObjectType):
    timestamp = graphene.String()
    message = graphene.String()
    author = graphene.String()
    commit_hash = graphene.String()

class Repository(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()
    original_author = graphene.String()
    branches = graphene.List(graphene.String)
    # commits = graphene.List(Commit)
