import os
import xml.etree.ElementTree as ET

file_path = "/data/xml/data.xml"

def get_data():
    try:
        # Datei öffnen und Inhalt lesen
        with open(os.getcwd() + file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except Exception as e:
        raise e
    
def add_new_product(xml_string: str):
    # XML-Datei einlesen
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Das neue Produkt aus dem String parsen
    new_product_fragment = ET.fromstring(f"<root>{xml_string}</root>")

    # Die Kinder des Fragments zum Haupt-XML hinzufügen
    for child in new_product_fragment:
        root.append(child)

    # Änderungen zurück in die Datei schreiben
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

    print("Das neue Produkt wurde erfolgreich hinzugefügt.")
