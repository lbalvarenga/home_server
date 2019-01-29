from flask import render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
import os

from . import files

@files.route("/upload/", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(os.getcwd(), file.filename))
    return redirect(request.referrer)

def fetch():
    pass