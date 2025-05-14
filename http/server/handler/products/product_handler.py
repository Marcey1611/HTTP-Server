import os
import xml.etree.ElementTree as ET  # Für die Verarbeitung und Manipulation von XML-Daten
import logging
from typing import List, Tuple

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType
from entity.exceptions import UnprocessableEntityException

# Pfad zur XML-Datei, die die Produktdaten speichert
file_path = os.getcwd() + "/handler/products/data.xml"

def get_products(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um alle oder gefilterte Produkte aus der XML-Datei zurückzugeben.
    """
    try:
        # Öffne und lese die XML-Datei
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        # Wenn eine Query vorhanden ist, filtere die Produkte
        if request.query:
            root = ET.fromstring(data)  # Parse den XML-Inhalt
            names, prices = parse_query(request.query)  # Query-Parameter extrahieren
            data = filter_in_xml(root, names, prices)  # Produkte filtern
            data = ET.tostring(data, encoding="utf-8").decode("utf-8")  # In String umwandeln

        # Setze Content-Type auf XML und erstelle die Antwort
        headers = {}
        headers["Content-Type"] = ContentType.XML.value
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        logging.error(e)
        raise e

def post_products(request: Request) -> Response:
    """
    Verarbeitet eine POST-Anfrage, um neue Produkte zur XML-Datei hinzuzufügen.
    """
    try:
        # Parse die bestehende XML-Datei
        tree = ET.parse(file_path)
        root = tree.getroot()

        try:
            # Parse den Body der Anfrage als neues Produkt
            new_product = ET.fromstring(f"<product>{request.body}</product>")
        except ET.ParseError:
            # Fehler bei ungültigem XML-Format
            raise UnprocessableEntityException("XML invalid.")

        # Füge das neue Produkt zur XML-Struktur hinzu
        root.append(new_product)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)  # Datei aktualisieren
        
        # Erfolgsantwort erstellen
        body = "Product(s) successfully created!"
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise e

def delete_products(request: Request) -> Response:
    """
    Verarbeitet eine DELETE-Anfrage, um Produkte basierend auf Query-Parametern zu löschen.
    """
    try:
        # Parse die bestehende XML-Datei
        tree = ET.parse(file_path)
        root = tree.getroot()
        names, prices = parse_query(request.query)  # Query-Parameter extrahieren

        # Produkte basierend auf Name oder Preis entfernen
        for product in root.findall("product"):
            name = product.find("name").text if product.find("name") is not None else None
            price = int(product.find("price").text) if product.find("price") is not None else None
            if (names and name in names) or (prices and price in prices):
                root.remove(product)

        # Aktualisierte XML-Datei speichern
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        body = "Product(s) successfully deleted."
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except Exception as e:
        logging.error(e)
        raise e

def put_products(request: Request) -> Response:
    """
    Verarbeitet eine PUT-Anfrage, um Produkte zu aktualisieren oder hinzuzufügen.
    """
    try:
        # Parse die bestehende XML-Datei
        tree = ET.parse(file_path)
        root = tree.getroot()

        try:
            # Parse die neuen Produktdaten aus dem Anfrage-Body
            new_products = ET.fromstring(request.body)
        except ET.ParseError:
            # Fehler bei ungültigem XML-Format
            raise UnprocessableEntityException("XML invalid.")

        # Durchlaufe die neuen Produkte und aktualisiere oder füge sie hinzu
        for new_product in new_products.findall("product"):
            new_name = new_product.find("name").text if new_product.find("name") is not None else None
            new_price = new_product.find("price").text if new_product.find("price") is not None else None

            if not new_name or not new_price:
                continue  # Überspringe ungültige Produkte

            # Überprüfe, ob das Produkt bereits existiert
            existing_product = None
            for product in root.findall("product"):
                name = product.find("name").text if product.find("name") is not None else None
                if name == new_name:
                    existing_product = product
                    break

            # Aktualisiere den Preis, falls das Produkt existiert, ansonsten füge es hinzu
            if existing_product:
                existing_product.find("price").text = new_price
            else:
                root.append(new_product)

        # Aktualisierte XML-Datei speichern
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        body = "Product(s) successfully updated or added."
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise e

def parse_query(query: str) -> Tuple[List[str], List[int]]:
    """
    Parst Query-Parameter, um Namen und Preise zu extrahieren.
    """
    try:
        queries = {}
        # Zerlege die Query in Schlüssel-Wert-Paare
        for pair in query.split('&'):
            key, value = pair.split('=', 1)
            if key in queries:
                queries[key].append(value)
            else:
                queries[key] = [value]

        # Namen und Preise extrahieren
        names = queries.get("name", [])
        prices = [int(price) for price in queries.get("price", [])]
        return names, prices
    except Exception as e:
        logging.error(e)
        raise e

def filter_in_xml(data: ET.Element, names: List[str], prices: List[int]) -> ET.Element:
    """
    Filtert Produkte aus der XML-Struktur basierend auf Namen und Preisen.
    """
    try:
        filtered_root = ET.Element("products")  # Neue Wurzel für gefilterte Produkte
        for product in data.findall("product"):
            name = product.find("name").text if product.find("name") is not None else None
            price = int(product.find("price").text) if product.find("price") is not None else None

            # Produkt filtern: nur hinzufügen, wenn es die Kriterien erfüllt
            if names and name not in names:
                continue
            if prices and price not in prices:
                continue

            filtered_root.append(product)
        return filtered_root
    except Exception as e:
        logging.error(e)
        raise e
