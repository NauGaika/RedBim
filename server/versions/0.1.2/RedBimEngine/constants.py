# -*- coding: utf-8 -*-
"""Хранятся константы.

USERNAME
HOME_DIR
DIR_SCRIPTS
STATIC_IMAGE
USER_SCRIPTS
LOGO
"""
import os


def get_username():
    """Получить текущее имя пользователя."""
    uname = __revit__.Application.Username
    uname = uname.split('@')[0]
    uname = uname.replace('.', '')
    return uname


def parent_dir(dir, count=1):
    """Получает родительску дирректорию."""
    dir_name = dir
    while count:
        count -= 1
        dir_name = os.path.dirname(dir_name)
        dir_name = os.path.abspath(dir_name)
    return dir_name

HOME_DIR = os.getenv('PROGRAMDATA')
REVIT_VERSION = __revit__.Application.VersionNumber
HOME_DIR = os.path.join(HOME_DIR, "Autodesk", "Revit", "Addins", REVIT_VERSION, "RedBim")

USERNAME = get_username()

LOADER = os.path.join(HOME_DIR, 'loader')

DIR_SCRIPTS = os.path.join(HOME_DIR, 'scripts')

STATIC_IMAGE = os.path.join(HOME_DIR, 'static\\img')

LOGO = 'RB'

START_SCRIPT = os.path.join(HOME_DIR, 'common_scripts\\start_of_script.py')

__all__ = ['USERNAME', 'HOME_DIR', 'DIR_SCRIPTS', 'STATIC_IMAGE', 'LOGO', 'START_SCRIPT', 'LOADER', "REVIT_VERSION"]
