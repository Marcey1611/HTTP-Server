import socket
import argparse
import logging

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def send_request(method, path, host, port, headers):
    # Verbindung aufbauen
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        #client_socket.bind(("localhost", 55555))
        client_socket.connect((host, port))
        logging.info("Verbindung hergestellt.")

        # Anfrage zusammenstellen
        request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        request += "\r\n"

        # Anfrage senden
        logging.info(f"Anfrage:\n{request}")
        client_socket.sendall(request.encode())

        # Antwort empfangen
        response = client_socket.recv(4096).decode()
        logging.info(f"Antwort:\n{response}")

        # Verbindung offen lassen, falls keep-alive unterstützt wird
        if headers.get("Connection", "").lower() == "keep-alive":
            logging.info("Verbindung bleibt geöffnet.")
        else:
            client_socket.close()
            logging.info("Verbindung geschlossen.")
    except socket.error as e:
        logging.error(f"Fehler: {e}")
    finally:
        if client_socket:
            client_socket.close()


def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description="HTTP-Client für GET-Anfragen")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    args = parser.parse_args()

    # Headers in ein Dictionary umwandeln
    headers = {}
    if args.headers:
        for header in args.headers:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()

    # Default-Header hinzufügen, falls nicht angegeben
    #if "Connection" not in headers:
    #    headers["Connection"] = "keep-alive"

    # Anfrage senden
    send_request(args.method, args.path, args.host, args.port, headers)


if __name__ == "__main__":
    main()
