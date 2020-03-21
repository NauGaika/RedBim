# -*- coding: utf-8 -*- 
import os

from flask import send_file, request
from server import app
from .RedBimUpdater import RedBimUpdater

rbu = RedBimUpdater()

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"
@app.route('/latest_version')
def latest_version():
    return rbu.latest_version.version

@app.route('/file_list')
def file_list():
    try:
        return send_file(rbu.latest_version.get_file_list(), attachment_filename=rbu.latest_version.version + ".json")
    except Exception as e:
        return str(e)

@app.route("/get_file", methods=["GET"])
def get_file():
    """Register user."""
    file_name = request.args.get('file')
    print(file_name)
    file_path = rbu.latest_version.get_file(file_name)
    if file_path:
        try:
            return send_file(file_path, attachment_filename=os.path.split(file_path)[1])
        except Exception as e:
            return str(e)
    return "Файл не найден в последней версии"