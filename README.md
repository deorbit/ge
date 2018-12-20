A simple GraphQL service that interacts with git repositories.

docker build -t ge .
docker run -i -t --rm -p 5000:5000 ge

Mutation:
http://localhost:5000/graphql?query=mutation%7B%0A%20%20cloneRepo(url%3A"https%3A%2F%2Fgithub.com%2Frequests%2Frequests")%7B%0A%20%20%20%20repository%20%7B%0A%20%20%20%20%20%20url%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20originalAuthor%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D

Repository Query;
http://localhost:5000/graphql?query=%7B%0Arepository(name%3A%20"requests")%20%7B%0A%20%20%20%20branches%0A%20%20%20%20originalAuthor%0A%20%20%7D%0A%7D

Commit Query:
http://localhost:5000/graphql?query=%7B%0Acommit(name%3A%22requests%22%2C%20hash%3A%228761e9736f7d5508a5547cdf3adecbe0b7306278%22)%20%7B%0A%20%20%20%20author%0A%20%20%20%20message%0A%20%20%20%20timestamp%0A%20%20%7D%0A%7D