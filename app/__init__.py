from flask import Flask
from elasticsearch import Elasticsearch
import os

es = Elasticsearch([{'host': os.environ.get('HOST'), 'port': os.environ.get('PORT')}])
print(es.ping())

app = Flask(__name__)

from . import views
