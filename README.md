# internet-project-ws2425

# Supported headers
- Connection: <code>keep-alive | close</code>
- Content-Type: <code>application/json | text/html | application/xml | text/plain</code>
- - necessary for post requests
- Content-Length: <code>length</code>
- User-Agent: <code>user-agent</code>
- - Simpler than in practice: "CustomClient" XD
- Host: <code>host</code>
- - In our http-server-client system example 127.0.0.1:8080 because the server and client are runing on our localhost.
- Accept: <code>application/json | text/html | application/xml | text/plain | ...</code>
- - Which data the client accepts as response value/body.

# Methods and Paths
- GET /
- GET /info
- GET /html
- GET /json
- GET /xml
- POST /json/add_new_user
- POST /xml/add_new_product
- POST /html/add_data
- DELETE /json/delete_user?name=<user>

# Available status codes
- 200, 201, 400, 404, 405, 406, 415, 422, 500

# Start the server
- python server.py

# Example Requests (By starting the client)
- <code>python client.py POST /json/add_user --host 127.0.0.1 --port 8080 --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":20}'</code>
- <code>python client.py POST /html/add_data --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:text/html" "Host:127.0.0.1:8080" --body '<div><p>TEST</p></div>'</code>
- <code>python client.py POST /xml/add_new_product --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:application/xml" "Host:127.0.0.1:8080" --body '<product>Test</product><price>100</price>'</code>

# Exmaple Requests (During Runtime of Client)
- <code>POST /json/add_user --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":100}'</code>


Fragen an Dozenten:
- Was wäre der aktuelle Stand ganz grob für ne Note?
- Müssen wir genau den Regeln von der HTTP Spezifikation folgen oder dürfen wir an manchen Stellen unsere eigenen Ideen einbringen? Stichwort: Keep-Alive Max-Requests in Response runterzählen
- Auf welchem OS muss der Server laufen? Windows oder Linux? Oder beides? Problem: Input-Thread des Clients -> Nichtblockierender Input -> Unterschiedliche Lösungen bei Linux und Windows