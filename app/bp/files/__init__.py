from flask import Blueprint
import os

files = Blueprint("files", __name__)

from . import routes