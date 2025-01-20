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
- - Will be set automatically by the client.
- Host: <code>host:port</code>
- - Required for every request.
- - If you run the server on the local machine it should be "127.0.0.1:8080" or "localhost:8080".
- Accept: <code>application/json | text/html | application/xml | text/plain | ...</code>
- - Which data the client accepts as response value/body. The server will check this header if it is working with the called ressource.
- Authorization: <code>Basic user:password</code>
- - Important: WWW-Authenticate header not supported yet. (keine Zeit mehr gehabt)
- - The client encodes in base64 so you can give him the plain user:password combination.
- - The password will be hashed and the server will check its hash table if the password hash is correct for the given user.
- - Authorization is not required with GET requests.

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
- - Here you can see the Readme.md of our project as html.
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

## How to start the Server
- python server.py

## How to start the client and sending the first request
You just can start the client and send the first request. It is not supported to start the client without sending a request. One runtime of the client will be one session with the server your calling. So the client will cancle if the session closed by the called server. You also can cancle the client with <code>STRG+C</code>.
We sill explain how to start the client by following exmaples:
- <code>python client.py GET / --host 127.0.0.1 --port 8080 --headers "Connection: keep-alive"</code>
- <code>python client.py POST /products --host 127.0.0.1 --port 8080 --headers "Content-Length: 54" "Content-Type:application/xml" --body '`<product><name>Test</name><price>100</price></product>`'</code>
- <code>python client.py DELETE /users?name=Max --host 127.0.0.1 --port 8080</code>

As you canmn see we starting the python script with <code>python client.py</code> and then we add the method and path which should be called: <code>GET /</code>, <code>POST /products</code> or <code>DELETE /users?name=Max</code>. After this we define the host and port of the host which should called <code>--host 127.0.0.1 --port 8080</code>. Then we can add some headers for example: <code>--headers "Connection: keep-alive"</code> (here we setting the headers Connection to keep-alive) or <code>--headers "Content-Length: 54" "Content-Type:application/xml"</code> (here we setting the length of the body as content-length and the content-type of the provided body). Finally we can add a body: <code>--body '`<product><name>Test</name><price>100</price></product>`'</code>

## How to handle the client during runtime
During the runtime you can simply use the commands from above just without the <code>python client.py</code> part, the --host and --port parameters and also without the Connection-Header because are now in a "Keep-Alive" session.

## The config- or validation-set of our http-server
{  
    "/": {  
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"],
            "handler": get_root
        }
    },
    "/info": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"],
            "handler": get_info
        }
    },
    "/info/routes": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info/headers": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/info/general": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/plain"]
        }
    },
    "/users": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": get_users
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["application/json"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": post_users
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["application/json"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/json"],
            "handler": put_users
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/json"],
            "handler": delete_users
        }
    },
    "/products": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"],
            "handler": get_products
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["application/xml"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"],
            "handler": post_products
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["application/xml"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "application/xml"],
            "handler": put_products
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "application/xml"],
            "handler": delete_products
        }
    },
    "/divs": {
        "GET": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": get_divs
        },
        "POST": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["text/html"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"],
            "handler": post_divs
        },
        "PUT": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"], "content-type": ["text/html"], "content-length": []},
            "body_required": True,
            "query_required": False,
            "query_allowed": False,
            "accept": ["*/*", "text/html"]
        },
        "DELETE": {
            "required_headers": {"host": ["127.0.0.1:8080", "localhost:8080"]},
            "body_required": False,
            "query_required": True,
            "query_allowed": True,
            "accept": ["*/*", "text/html"]
        }
    }
}
