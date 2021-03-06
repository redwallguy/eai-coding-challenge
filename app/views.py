from . import app, logic
from werkzeug.routing import BaseConverter
from flask import request
import json


class NameConverter(BaseConverter):
    def __init__(self, url_map):
        super(NameConverter, self).__init__(url_map)
        self.regex = r'\w{1,15}'


app.url_map.converters['name_reg'] = NameConverter


@app.route('/contact/<name_reg:username>', methods=['GET', 'PUT', 'DELETE'])
def exists_handler(username):
    if request.method == 'GET':
        return json.dumps(logic.get_contact(username))
    if request.method == 'PUT':
        return logic.update_contact(username, request.get_json())
    if request.method == 'DELETE':
        return logic.delete_contact(username)


@app.route('/contact', methods=['GET', 'POST'])
def base_handler():
    if request.method == 'POST':
        req = request.get_json()
        if 'name' not in req:
            return json.dumps(req)
        if logic.get_contact(req['name']) == logic.contact_not_found_dict:
            logic.create_contact(req)
            return "Success. " + req['name'] + " was added."
        return "Sorry. That name is already taken."
    if request.method == 'GET':
        argd = [request.args.get('pageSize'), request.args.get('page'), request.args.get('q')]
        if all(n is not None for n in argd):
            res = logic.get_index(argd[0], argd[1], argd[2])
            if res["hits"]["total"] == 0:
                return "No contacts currently exist."
            response_str = ""
            for hit in res["hits"]["hits"]:
                response_str += json.dumps(hit["_source"]) + "\n"
            return response_str
        return json.dumps(request.args)
