### internet-project-ws2425

# Server

## Gneral Information
- The server runs on port 8080.

## Supported Request Headers
- Connection: <code>keep-alive | close</code>
- - The server supports keep-alive.
- Content-Type: <code>application/json | text/html | application/xml</code>
- - Required for PUT and POST requests.
- Content-Length: <code>length</code>
- - Required for PUT and POST requests.
- Host: <code>host:port</code>
- - Required for every request.
- - If you run the server on the local machine it should be "127.0.0.1:8080" or "localhost:8080".
- Accept: <code>application/json | text/html | application/xml | text/plain | ...</code>
- - Which data the client accepts as response value/body. The server will check this header if it is working with the called ressource.

## Supported Response Headers
- Connection: <code>keep-alive | close</code>
- - In case of a connection keep-alive header in the request, in the "Sub"-Header "Keep-Alive" will be informations about the Keep-Alive-Process (because of HTTP/1.1).
- Content-Type: <code>application/json | text/html | application/xml | text/plain</code>
- - Which type the response body is.
- Content-Length: <code>length</code>
- - Length of the response body.
- Allow: <code>GET, POST, PUT, DELTE</code>
- - In case of an 405er here will be the allowed methods.
- Date: <code>Sun, 19 Jan 2025 18:18:05 GMT</code>
- - The time when the response was sent.

## Paths and their allowed Methods
- <code>/</code> Allowed Methods
- - <code>GET</code> - query not allwowed, no body required
- <code>/info</code> Allowed Methods:
- - <code>GET</code> - query not allwowed, no body required
- <code>/users</code> Allowed Methods:
- - <code>GET</code> - query allowed, no body required
- - <code>POST</code> - query not allowed, body required
- - <code>PUT</code> - query not allowed, body required
- - <code>DELETE</code> - query allowed, no body required
- <code>/products</code> Allowed Methods:
- - <code>GET</code> - query allowed, no body required
- - <code>POST</code> - query not allowed, body required
- - <code>PUT</code> - query not allowed, body required
- - <code>DELETE</code> - query allowed, no body required
- <code>/divs</code> Allowed Methods:
- - <code>GET</code> - query not allowed, no body required
- - <code>POST</code> - query not allowed, body required


## Supported status codes (for error handling)
- <code>200 OK</code>
- <code>400 Bad Request</code>
- <code>404 Not Found</code>
- <code>405 Method Not Allowed</code>
- <code>406 Not Acceptable</code>
- <code>411 Length Required</code>
- <code>413 Payload Too Large</code>
- <code>415 Unsupported Media Type</code>
- <code>422 Unprocessable Entity</code>
- <code>500 Internal Server Error</code>
- <code>501 Not Implemented</code>

## Start the server
- python server.py

## Example Requests (By starting the client)
- <code>python client.py POST /json/add_user --host 127.0.0.1 --port 8080 --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":20}'</code>
- <code>python client.py POST /html/add_data --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:text/html" "Host:127.0.0.1:8080" --body '<div><p>TEST</p></div>'</code>
- <code>python client.py POST /xml/add_new_product --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:application/xml" "Host:127.0.0.1:8080" --body '<product>Test</product><price>100</price>'</code>

## Exmaple Requests (During Runtime of Client)
- <code>POST /json/add_user --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":100}'</code>
