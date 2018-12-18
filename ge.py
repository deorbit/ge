from flask import Flask
from flask_graphql import GraphQLView
import graphene
from gapi.query import GiQuery
from gapi.mutation import GiMutations

app = Flask("ge")
schema = graphene.Schema(query=GiQuery, mutation=GiMutations)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

def main():
    app.run()

if __name__ == '__main__':
    main()