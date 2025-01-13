# internet-project-ws2425

# Supported headers
Client:
- Connection: keep-alive | close
- Content-Type: application/json | text/html | application/xml
- - necessary for post requests
- Content-Length: <length>
- User-Agent: <user-agent>
- - Simpler than in practice: "CustomClient" XD
- Host: <host>
- - In our http-server-client system example 127.0.0.1:8080 because the server and client are runing on our localhost.

# Methods and Paths
- GET /
- GET /info
- GET /html
- GET /json
- GET /xml
- POST /json/add_user