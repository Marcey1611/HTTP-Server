# internet-project-ws2425

# Supported headers
Client:
- Connection: keep-alive | close
- Content-Type: application/json | text/html | application/xml | text/plain
- - necessary for post requests
- Content-Length
- User-Agent
- - Simpler than in practice: "CustomClient" XD
- Host
- - In our http-server-client system example 127.0.0.1:8080 because the server and client are runing on our localhost.
- Accept: Ehich data the client accepts as response value/body.

# Methods and Paths
- GET /
- GET /info
- GET /html
- GET /json
- GET /xml
- POST /json/add_user

# Example Requests (Start)
- <code>python client.py POST /json/add_user --host 127.0.0.1 --port 8080 --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":20}'</code>
- python client.py POST /html/add_data --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:text/html" "Host:127.0.0.1:8080" --body '<div><p>TEST</p></div>'
- python client.py POST /xml/add_new_product --host 127.0.0.1 --port 8080 --headers "User-Agent:CustomClient" "Connection:keep-alive" "Content-Type:application/xml" "Host:127.0.0.1:8080" --body '<product>Test</product><price>100</price>'

# Exmaple Requests (During Runtime of Client)
- <code>POST /json/add_user --headers "Connection:keep-alive" "Content-Type:application/json" "Host:127.0.0.1:8080" --body '{\"name\":\"Test\",\"age\":100}'</code>


Fragen an Dozenten:
- Was wäre der aktuelle Stand ganz grob für ne Note?
- Dürfen wir auch keine Libraries wie logging verwenden oder ist das in Ordnung?
- Müssen wir genau den Regeln von der HTTP Spezifikation folgen oder dürfen wir an manchen Stellen unsere eigenen Ideen einbringen? Stichwort: Keep-Alive Max-Requests in Response runterzählen
- Auf welchem OS muss der Server laufen? Windows oder Linus? Oder beides? Problem: Input-Thread des Clients -> Nichtblockierender Input -> Unterschiedliche Lösungen bei Linux und Windows