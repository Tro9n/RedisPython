from models.model_redis import connection
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
import random
import json


app = Flask(__name__)
api = Api(app)


@app.route('/')
def manage_items(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in connection.keys("*"):
            items[key.decode("utf-8")] = connection.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        connection.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)


if __name__ == "__main__":
    app.run()