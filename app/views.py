from . import app, logic
from werkzeug.routing import BaseConverter
from flask import request
import json


class NameConverter(BaseConverter):
    def __init__(self, url_map):
        super(NameConverter, self).__init__(url_map)
        self.regex = r'\w{1,15}'


app.url_map.converters['name_reg'] = NameConverter


@app.route('/')
@app.route('/index')
def index():
    return "+play ssf"


@app.route('/contact/<name_reg:username>', methods=['GET', 'PUT', 'DELETE'])
def exists_handler(username):
    if request.method == 'GET':
        return json.dumps(logic.get_contact(username))
    if request.method == 'PUT':
        return logic.update_contact(username, request.get_json())
    if request.method == 'DELETE':
        return logic.delete_contact(username)


@app.route('/contact', methods=['POST'])
def create_handler():
    req = request.get_json()
    if 'name' not in req:
        return json.dumps(req)
    if logic.get_contact(req['name']) == logic.contact_not_found_dict:
        logic.create_contact(req)
        return "Success. " + req['name'] + " was added."
    return "Sorry. That name is already taken."
