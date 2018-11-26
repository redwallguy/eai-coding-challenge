import re
from . import es
import json

contact_not_found_dict = {"error": "Contact not found."}


class Contact:
    name_regex = re.compile(r'^\w{1,15}$')
    phone_regex = re.compile(r'^\d{7,13}$')
    min_age = 0
    max_age = 150

    def __init__(self, name, phone_num=None, age=18):
        if self.name_regex.match(name) is not None:
            self.name = name
        else:
            self.name = 'John'
        if phone_num is None:
            pass
        elif self.phone_regex.match(phone_num) is not None:
            self.phone_num = phone_num
        if self.min_age <= age <= self.max_age:
            self.age = age
        else:
            self.age = 18


def create_contact(form):
    name=form['name']
    phone_num=None
    age=18
    if 'phone_num' in form:
        phone_num = form['phone_num']
    if 'age' in form:
        age = int(form['age'])
    es.index(index='contact', doc_type='_doc', body=json.dumps(Contact(name, phone_num, age).__dict__))


def update_contact(name, form):
    contact_id = get_contact_id(name)
    if contact_id != contact_not_found_dict:
        phone_num = None
        age = 18
        if 'phone_num' in form:
            phone_num = form['phone_num']
        if 'age' in form:
            age = int(form['age'])
        es.index(index='contact', doc_type='_doc', id=contact_id,
                 body=json.dumps(Contact(name, phone_num, age).__dict__))
        return "Success. " + name + " was updated."
    return json.dumps(contact_not_found_dict)


def delete_contact(name):
    if get_contact(name) != contact_not_found_dict:
        query_string = json.dumps( \
            {"query": {
                "bool": {
                    "must": [
                        {"match": {
                            "name": name
                        }}
                    ]
                }
            }})
        es.delete_by_query(index=("contact",), body=query_string)
        return "Success."
    return json.dumps(contact_not_found_dict)


def get_contact(name):
    query_string = json.dumps(\
    {"query": {
        "bool": {
            "must": [
                {"match": {
                    "name": name
                }}
            ]
        }
    }})
    res = es.search(index=("contact",), body=query_string)
    if res["hits"]["total"] == 0:
        return contact_not_found_dict
    return res["hits"]["hits"][0]["_source"]


def get_contact_id(name):
    query_string = json.dumps( \
        {"query": {
            "bool": {
                "must": [
                    {"match": {
                        "name": name
                    }}
                ]
            }
        }})
    res = es.search(index=("contact",), body=query_string)
    if res["hits"]["total"] == 0:
        return contact_not_found_dict
    return res["hits"]["hits"][0]["_id"]


def get_index(size, offset, qsq):
    return es.search(index=("contact",), size=size, from_=offset, q=qsq)
