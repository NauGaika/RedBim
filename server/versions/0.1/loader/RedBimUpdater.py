﻿# -*- coding: utf-8 -*-
import urllib
import json
import os

class RedBimUpdater:
    "Выполняет обновление плагина"
    def __init__(self, system_path):
        self.SYSTEM_PATH = system_path
        self.SERVER_URL = r"http://redbim.ru"
        self.SERVER_GET_VERSION = r"/latest_version"
        self.SERVER_GET_FILE_LIST = r"/file_list"
        self.SERVER_GET_REDBIM_FILE = r"/get_file"
        self.SERVER_SAY_HI = r"/say_hi"
        self.VERSION_FILE = "config.conf"
        self.say_hi(__revit__.Application.Username)
        if self.system_version is None or (self.server_version is not None and self.system_version != self.server_version):
            self.update_RedBim()
        print("Запускаем RedBim")

    def say_hi(self, username):
        if not username:
            username = "Пользователь не определен"
        username = urllib.quote(username.encode('utf8'), ':/')
        if not username:
            username = "user_not_find"
        url = self.SERVER_URL + self.SERVER_SAY_HI + "?user=" + username
        response = urllib.urlopen(url)

    @property
    def config(self):
        config = os.path.join(self.SYSTEM_PATH, self.VERSION_FILE)
        if os.path.exists(config):
            return True

    @property
    def system_version(self):
        if self.config:
            return True

    @property
    def server_version(self):
        if not hasattr(self, "_server_version"):
            try:
                response = urllib.urlopen(self.SERVER_URL + self.SERVER_GET_VERSION)
                self._server_version = response.read()
                response.close()
                return res
            except:
                self._server_version = None
                print("Ошибка получения версии на сервере")
        return self._server_version

    def update_RedBim(self):
        all_files = self.get_all_files_without_exept(self.SYSTEM_PATH)
        if self.server_file_list:
            self.compare_file_lists(self.server_file_list, all_files)

    def compare_file_lists(self, server_dict, client_dict):
        with open(os.path.join(self.SYSTEM_PATH, "update_log.txt"), "wb") as log:
            log.write("Получили файлы с сервера \n".encode("utf-8"))
            for i in server_dict.keys():
                log.write("Проверяем файл с сервера {} \n".format(i).encode("utf-8"))
                new_file = i not in client_dict.keys()
                if new_file:
                    log.write("Определен как новый \n".encode("utf-8"))
                else:
                    log.write("Такой уже есть \n".encode("utf-8"))
                old_file = None
                if not new_file:
                    print(client_dict[i])
                    old_file = int(client_dict[i]) < int(server_dict[i])
                    to_write = "Сверяем время серверной время {} Клиентское время {} \n".format(int(server_dict[i]), int(client_dict[i]))
                    log.write(to_write.encode("utf-8"))
                    if old_file:
                        log.write("Нужно обновить \n".encode("utf-8"))
                if new_file or old_file:
                    try:
                        file_path = os.path.join(self.SYSTEM_PATH, i)
                        dir_path = os.path.split(file_path)[0]
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        file = self.server_get_file(i)
                        with open(file_path, "wb") as f:
                            f.write(file)
                            f.close()
                        if new_file:
                            print("Создан новый файл " + file_path)
                        elif old_file:
                            print("Обновлен файл " + file_path)
                    except:
                        print("Ошибка создания/обновления файла " + file_path)
            log.close()

    def server_get_file(self, file):
        try:
            file = file.replace("\\", "/")
            file = urllib.quote(file.encode('utf8'), ':/')
            url = self.SERVER_URL + self.SERVER_GET_REDBIM_FILE + "?file=" + file
            response = urllib.urlopen(url)
            res = response.read()
            return res
        except:
            "Не удалось получить файл " + file

    @property
    def server_file_list(self):
        if not hasattr(self, "_server_file_list"):
            try:
                response = urllib.urlopen(self.SERVER_URL + self.SERVER_GET_FILE_LIST)
                self._server_file_list = response.read()
                response.close()
                self._server_file_list = json.loads(self._server_file_list.decode("utf-8"))
                self._server_file_list = {key.replace("/", "\\"): i for key, i in self._server_file_list.items()}
            except:
                self._server_file_list = None
        return self._server_file_list

    def get_all_files_without_exept(self, path, except_dir=[], except_file=[], result=None, gen_path_len=0):
        return_res = False
        if result is None:
            result = {}
            return_res = True
            gen_path_len = len(path) + 1
        for i in os.listdir(path):
            curpath = os.path.join(path, i)
            if os.path.isdir(curpath):
                self.get_all_files_without_exept(curpath, except_dir=except_dir, except_file=except_file, result=result)
            else:
                result.update({curpath: os.stat(curpath).st_mtime})
        if return_res:
            result = {key[gen_path_len:]: i for key, i in result.items()}
            return result
