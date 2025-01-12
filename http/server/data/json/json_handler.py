import json

# Datei-Pfad zur JSON-Datei
file_path = 'data.json'

def add_new_user(new_user):
    # JSON-File einlesen
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Bestehendes JSON-Objekt laden
    except FileNotFoundError:
        # Falls Datei nicht existiert, neues JSON-Objekt erstellen
        data = {"users": []}

    # JSON-String in ein Python-Objekt umwandeln
    new_data = json.loads(new_user)

    # Neuen Benutzer hinzufügen
    data["users"].append(new_data)

    # Aktualisiertes JSON-Objekt zurück in die Datei schreiben
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Schön formatieren mit Einrückung
