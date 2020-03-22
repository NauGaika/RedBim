# -*- coding: utf-8 -*- 
import os
import re
import json

class RedBim_Version:
    VERSION_PATH = os.path.abspath(os.path.join("server", "versions"))
    FILE_LIST_NAME = r"files.json"
    LATEST_VERSION = None

    def __init__(self, version):
        self.version = version

    @classmethod
    def get_latest_version(cls):
        print(cls.VERSION_PATH)
        files = [i for i in os.listdir(cls.VERSION_PATH) if os.path.isdir(os.path.join(cls.VERSION_PATH, i))]
        files.sort(key=lambda x: os.stat(os.path.join(cls.VERSION_PATH, x)).st_mtime, reverse=True)
        if cls.LATEST_VERSION is None or cls.LATEST_VERSION.version != files[0]:
            cls.LATEST_VERSION = cls(files[0])
        return cls.LATEST_VERSION

    @property
    def file_list_path(self):
        return os.path.abspath(os.path.join(self.VERSION_PATH, self.version, self.FILE_LIST_NAME))

    @property
    def version_path(self):
        return os.path.join(self.VERSION_PATH, self.version)
    
    def get_file_list(self):
        "Возвращает путь к файлу, который нужно вернуть пользователю."
        if not os.path.exists(self.file_list_path):
            self.create_file_list()
        return self.file_list_path

    def create_file_list(self):
        "Создает json file с версиями файлов."
        files = self.find_all_files(self.version_path)
        with open(self.file_list_path, 'w', encoding='utf-8') as f:
            json.dump(files, f, indent=4, ensure_ascii=False)
            f.close()

    def get_file(self, file):
        file_version = os.path.join(self.version_path, file)
        if os.path.exists(file_version):
            return os.path.abspath(file_version)


    def find_all_files(self, path, except_dir=[], except_file=[], result=None, gen_path_len=0):
        "Рекурсивно находим все файлы в папке."
        return_res = False
        if result is None:
            result = {}
            return_res = True
            gen_path_len = len(path) + 1
        for i in os.listdir(path):
            curpath = os.path.join(path, i)
            if os.path.isdir(curpath):
                self.find_all_files(curpath, except_dir=except_dir, except_file=except_file, result=result)
            else:
                result.update({curpath: os.stat(curpath).st_mtime})
        if return_res:
            result = {key[gen_path_len:]: i for key, i in result.items()}
            return result

    def __repr__(self):
        return "Версия RedBim {}".format(self.version)
    

class RedBimUpdater:

    @property
    def latest_version(self):
        return RedBim_Version.get_latest_version()
    

