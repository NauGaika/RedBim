# -*- coding: utf-8 -*- 
import os

from flask import send_file, request
from server import app
from .RedBimUpdater import RedBimUpdater

rbu = RedBimUpdater()

@app.route('/')
@app.route('/index')
def index():
    return "Здесь будет сайт RedBim"

@app.route('/say_hi', methods=["GET"])
def say_hi():
    user = request.args.get('user')
    print(user)

@app.route('/say_hi', methods=["GET"])
def say_hi():
    user = request.args.get('user')
    print(user)

@app.route('/plagin', methods=["GET"])
def get_plagin():
    plagin = request.args.get('plagin')
    username = request.args.get('username')
    print(plagin, username)

@app.route('/latest_version')
def latest_version():
    print("Получаем версию")
    return rbu.latest_version.version

@app.route('/file_list')
def file_list():
    print("Получаем список файлов")
    try:
        return send_file(rbu.latest_version.get_file_list(), attachment_filename=rbu.latest_version.version + ".json")
    except Exception as e:
        pring(e)
        return str(e)

@app.route("/get_file", methods=["GET"])
def get_file():
    """Получение файла."""
    file_name = request.args.get('file')
    file_path = rbu.latest_version.get_file(file_name)
    print(file_path)
    if file_path:
        try:
            return send_file(file_path, attachment_filename=os.path.split(file_path)[1])
        except Exception as e:
            return str(e)
    return "Файл не найден в последней версии"