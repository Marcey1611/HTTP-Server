import os
import xml.etree.ElementTree as ET
import logging

from entity.models import Response, Request

file_path = os.getcwd()+"/handler/products/data.xml"

def get_products(request: Request) -> Response:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return Response("HTTP/1.1 200 OK", "application/xml", data, len(data))
    except Exception as e:
        raise e
    
def post_products(request: Request) -> Response:
    try:
        # XML-Datei einlesen
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Das neue Produkt aus dem String parsen
        new_product_fragment = ET.fromstring(f"<root>{request.xml_string}</root>")

        # Die Kinder des Fragments zum Haupt-XML hinzufügen
        for child in new_product_fragment:
            root.append(child)

        # Änderungen zurück in die Datei schreiben
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    except Exception as e:
        logging.error(e)
        raise e
