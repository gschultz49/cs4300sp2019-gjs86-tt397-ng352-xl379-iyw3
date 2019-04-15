import os 
# Import flask deps
from flask import request, render_template, \
	flash, g, session, redirect, url_for, jsonify, abort

# For decorators around routes
from functools import wraps 

# Import for pass / encryption 
from werkzeug import check_password_hash, generate_password_hash 

# Import the db object from main app module
from app import db 

# Marshmallow 
from marshmallow import ValidationError

# Import socketio for socket creation in this module 
from app import socketio

# Import module models 
from app.irsystem.models import *

# IMPORT THE BLUEPRINT APP OBJECT 
from app.irsystem import irsystem 

# Import module models
from app.accounts.models.user import *
from app.accounts.models.session import *


# # __file__ refers to the file settings.py
# APP_ROOT = os.path.dirname(os.path.abspath(
#     __file__))   # refers to application_top
# APP_STATIC = os.path.join(APP_ROOT, 'static')
