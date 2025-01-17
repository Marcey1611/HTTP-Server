import socket
import argparse
import logging
import multiprocessing
import sys
import time
import threading

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def send_request(client_socket, method, path, host, headers):
    """
    Sendet eine HTTP-Anfrage und gibt die Antwort zurück.
    """
    try:
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
        
        # Falls keine Antwort empfangen wird, Verbindung als verloren betrachten
        if not response:
            logging.error("Verbindung wurde vom Server geschlossen. Beende den Client.")
            return None
        return response
    except socket.error as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        return None


def parse_args():
    parser = argparse.ArgumentParser(description="Einfacher HTTP-Client")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    return parser.parse_args()


def convert_headers_to_dict(args):
    headers = {}
    if args.headers:
        for header in args.headers:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers


def create_connection(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))
    logging.info(f"Verbindung zu {args.host}:{args.port} hergestellt.")
    return client_socket


def monitor_connection(client_socket, stop_event, input_process):
    """
    Überwacht die Verbindung während der Eingabe.
    """
    while not stop_event.is_set():
        try:
            data = client_socket.recv(4096)
            if not data:  # Keine Daten empfangen -> Verbindung geschlossen
                logging.error("Verbindung wurde vom Server geschlossen. Beende den Client.")
                stop_event.set()
                input_process.terminate()
                input_process.join()
                break
        except socket.error as e:
            logging.error(f"Fehler beim Überwachen der Verbindung: {e}")
            stop_event.set()
            input_process.terminate()
            input_process.join()
            break
        time.sleep(1)


def input_function(stop_event, client_socket, headers, args):
    """
    Funktion für den Benutzereingabe-Prozess.
    """
    while not stop_event.is_set():
        try:
            user_input = input("\nGib eine neue Anfrage ein (z. B. GET /) oder 'exit' zum Beenden: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                logging.info("Beenden des Clients...")
                stop_event.set()
                break

            # Anfragen parsen und senden
            try:
                method, path = user_input.split()
                response = send_request(client_socket, method, path, args.host, headers)

                # Falls keine Antwort empfangen wurde (Verbindung geschlossen), stoppen
                if not response:
                    stop_event.set()
                    break
            except ValueError:
                logging.error("Ungültige Eingabe! Beispiel: GET /")
        except KeyboardInterrupt:
            logging.info("Benutzerabbruch. Beende den Client...")
            stop_event.set()
            break


def main():
    args = parse_args()
    headers = convert_headers_to_dict(args)

    try:
        client_socket = create_connection(args)

        # Erster Request sofort nach Verbindung
        response = send_request(client_socket, args.method, args.path, args.host, headers)

        # Keine Keep-Alive-Logik oder Timeout-Überwachung mehr
        logging.info("Keep-Alive wird ignoriert, der Client wartet auf die Eingabe des Nutzers.")

        # Stop-Ereignis für den Eingabe-Prozess
        stop_event = multiprocessing.Event()

        # Prozess für Benutzereingaben starten
        input_process = multiprocessing.Process(target=input_function, args=(stop_event, client_socket, headers, args))
        input_process.start()
        
         # Thread für die Überwachung der Verbindung starten
        monitor_thread = threading.Thread(target=monitor_connection, args=(client_socket, stop_event, input_process), daemon=True)
        monitor_thread.start()

        # Warten, bis der Prozess beendet wird
        input_process.join()  # Warte, bis der Eingabe-Prozess beendet wird

    except socket.error as e:
        logging.error(f"Socket-Fehler: {e}")
    finally:
        logging.info("Beende den Client...")
        stop_event.set()  # Setze das Stop-Ereignis, um alle Prozesse zu beenden
        if client_socket.fileno() != -1:
            client_socket.close()
        logging.info("Verbindung geschlossen.")


if __name__ == "__main__":
    main()
