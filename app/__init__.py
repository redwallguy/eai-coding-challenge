from flask import Flask
from elasticsearch import Elasticsearch
import os

es = Elasticsearch([{'host': os.environ.get('HOST'), 'port': os.environ.get('PORT')}])

app = Flask(__name__)

from . import views
