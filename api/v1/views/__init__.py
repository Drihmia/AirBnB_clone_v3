#!/usr/bin/python3
"""init file for views directory
creating the blueprint"""
from flask import Blueprint


app_views = Blueprint('first_blueprint',
                      __name__, url_prefix='/api/v1')
from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.states import *
from api.v1.views.amenities import *
=======
from api.v1.views.cities import *
>>>>>>> origin/storage_get_count
