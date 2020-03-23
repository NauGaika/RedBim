# -*- coding: utf-8 -*- 
import os
import datetime


from flask import send_file, request
from server import app
from .RedBimUpdater import RedBimUpdater

rbu = RedBimUpdater()
LOG_FILE = os.path.dirname(__file__)
LOG_FILE = os.path.join(LOG_FILE, "log.txt")

def print_in_log(*text):
    with open(LOG_FILE, "a") as f:
        now = datetime.datetime.now()
        all_text = ""
        for i in text:
            all_text += str(i)
        time_str = now.strftime("[%d-%m-%Y %H:%M] ")
        all_text = time_str + all_text + "</br>"
        f.write(all_text)
        f.close()

@app.route('/')
@app.route('/index')
def index():
    print_in_log("Зашли на главную страницу")
    return "Здесь будет сайт RedBim"

@app.route('/log')
def log_file():
    with open(LOG_FILE, "r") as f:
        text = f.read()
        f.close()
    return text

@app.route('/say_hi', methods=["GET"])
def say_hi():
    user = request.args.get('user')
    print_in_log(user)
    return "ok"

@app.route('/plagin', methods=["GET"])
def get_plagin():
    plagin = request.args.get('plagin')
    username = request.args.get('username')
    print_in_log(plagin, username)
    return "ok"

@app.route('/latest_version')
def latest_version():
    print_in_log("Получаем версию")
    return rbu.latest_version.version

@app.route('/file_list')
def file_list():
    print_in_log("Получаем список файлов")
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
    print_in_log(file_path)
    if file_path:
        try:
            return send_file(file_path, attachment_filename=os.path.split(file_path)[1])
        except Exception as e:
            return str(e)
    return "Файл не найден в последней версии"

@app.route("/download/redbim.rar")
def get_redbim():
    """Получение файла."""
    file = os.path.abspath(os.path.join("server", "static", "redbim.rar"))
    print_in_log("Загрузили RedBim")
    try:
        return send_file(file, mimetype="application/vnd.rar")
    except Exception as e:
        return str(e)