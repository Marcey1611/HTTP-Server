import os
import xml.etree.ElementTree as ET
import logging
from typing import List, Tuple

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType

file_path = os.getcwd()+"/handler/products/data.xml"

def get_products(request: Request) -> Response:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        if request.query:
            root = ET.fromstring(data)
            names, prices = parse_query(request.query)
            data = filter_in_xml(root, names, prices)
            data = ET.tostring(data, encoding="utf-8").decode("utf-8")
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.JSON.value, data, len(data))
    except Exception as e:
        raise e
    
def post_products(request: Request) -> Response:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        new_product = ET.fromstring(f"<product>{request.body}</product>")
        root.append(new_product)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        
        body = "Product(s) successfully created!"
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e
    
def delete_products(request: Request) -> Response:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        names, prices = parse_query(request.query)

        for product in root.findall("product"):
            name = product.find("name").text if product.find("name") is not None else None
            price = int(product.find("price").text) if product.find("price") is not None else None
            if (names and name in names) or (prices and price in prices):
                root.remove(product)

        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        body = "Product(s) successfully deleted."
        return Response("HTTP/1.1 " + HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e

def put_products(request: Request) -> Response:
    try:
        # Parse the existing XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Parse the new products from the request body (assuming it's in valid XML format)
        new_products = ET.fromstring(request.body)

        # Update existing products or add new ones
        for new_product in new_products.findall("product"):
            new_name = new_product.find("name").text if new_product.find("name") is not None else None
            new_price = new_product.find("price").text if new_product.find("price") is not None else None

            if not new_name or not new_price:
                continue

            existing_product = None
            for product in root.findall("product"):
                name = product.find("name").text if product.find("name") is not None else None
                if name == new_name:
                    existing_product = product
                    break

            if existing_product:
                existing_product.find("price").text = new_price
            else:
                root.append(new_product)

        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        body = "Product(s) successfully updated or added."
        return Response("HTTP/1.1 " + HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e


def parse_query(query: str) -> Tuple[List[str], List[int]]:
    try:
        queries = {}
        for pair in query.split('&'):
            key, value = pair.split('=', 1)
            if key in queries:
                queries[key].append(value)
            else:
                queries[key] = [value]

        names = queries.get("name", [])
        prices = [int(price) for price in queries.get("price", [])]
        return names, prices
    except Exception as e:
        logging.error(e)
        raise e

def filter_in_xml(data: ET.Element, names: List[str], prices: List[int]) -> ET.Element:
    try:
        filtered_root = ET.Element("products")
        for product in data.findall("product"):
            name = product.find("name").text if product.find("name") is not None else None
            price = int(product.find("price").text) if product.find("price") is not None else None

            if names and name not in names:
                continue
            if prices and price not in prices:
                continue

            filtered_root.append(product)
        return filtered_root
    except Exception as e:
        logging.error(e)
        raise e

'''def filter_out_xml(data: ET.Element, names: List[str], prices: List[int]) -> ET.Element:
    try:
        filtered_root = ET.Element("products")
        for product in data.findall("product"):
            name = product.find("name").text if product.find("name") is not None else None
            price = int(product.find("age").text) if product.find("age") is not None else None

            if names and name in names:
                continue
            if prices and price in prices:
                continue

            filtered_root.append(product)
        return filtered_root
    except Exception as e:
        logging.error(e)
        raise e'''