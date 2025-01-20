import json
import os
import logging

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType
from entity.exceptions import BadRequestException, UnprocessableEntityException
from typing import List

file_path = os.getcwd() + '/handler/users/data.json'

def get_users(request: Request) -> Response:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Kein useres in datei")
            raise Exception # 500er

        if request.query:
            names,ages = parse_query(request.query)
            data = filter_in(data, names, ages)

        data = json.dumps(data, ensure_ascii=False, indent=4)
        headers = {}
        headers['Content-Type'] = ContentType.JSON.value
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        raise e

def post_users(request: Request) -> Response:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        try:
            new_data = json.loads(request.body)
        except json.JSONDecodeError:
            raise UnprocessableEntityException("Invalid JSON.")

        data["users"].append(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        body = "User(s) successfully created."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as exception:
        raise exception
    except Exception as e:
        logging.error(e)
        raise e

def delete_users(request: Request) -> Response:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Kein useres in datei")
            raise Exception # 500er
        
        names, ages = parse_query(request.query)
        filtered_users = filter_out(data, names, ages)

        data["users"] = filtered_users

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        body = "User(s) successfully deleted."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except Exception as e:
        logging.error(e)
        raise e
    
def put_users(request: Request) -> Response:
    try:
        try:
            users = json.loads(request.body)
        except json.JSONDecodeError:
            raise UnprocessableEntityException("Invalid JSON.")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Kein useres in datei")
            raise Exception # 500er

        if not isinstance(users, list):
            raise BadRequestException()
        
        for user in users:
            if not isinstance(user, dict) or "name" not in user or "age" not in user:
                raise BadRequestException()

            existing_user = next((u for u in data["users"] if u["name"] == user["name"]), None)
            
            if existing_user:
                existing_user["age"] = user["age"]
            else:
                data["users"].append(user)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        body = "User(s) successfully updated or added."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as exception:
        raise exception        
    except Exception as e:
        logging.error(e)
        raise e
    
def parse_query(query: str) -> list:
    try:
        queries = {}
        for pair in query.split('&'):
            key, value = pair.split('=', 1)
            if key in queries:
                queries[key].append(value)
            else:
                queries[key] = [value]

        names = [str]
        ages = [int]

        names = queries.get("name", [])
        ages = [int(age) for age in queries.get("age", [])]
        return names,ages
    except Exception as e:
        logging.error(e)
        raise e

def filter_in(data: json, names: List[str], ages: List[int]):
    try:
        filtered_users = []
        for user in data.get("users"):
            if names and user.get("name") not in names:
                continue
            if ages and user.get("age") not in ages:
                continue
            filtered_users.append(user)
        return filtered_users
    except Exception as e:
        logging.error(e)
        raise e

def filter_out(data: json, names: List[str], ages: List[int]):
    try:
        filtered_users = []
        for user in data.get("users"):
            if names and user.get("name") in names:
                continue
            if ages and user.get("age") in ages:
                continue
            filtered_users.append(user)
        return filtered_users
    except Exception as e:
        logging.error(e)
        raise e
