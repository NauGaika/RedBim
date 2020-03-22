# -*- coding: utf-8 -*-
import clr, sys, os
import urllib

HOME_DIR = os.getenv('PROGRAMDATA')
REVIT_VERSION = __revit__.Application.VersionNumber
HOME_DIR = os.path.join(HOME_DIR, "Autodesk", "Revit", "Addins", REVIT_VERSION, "RedBim")


sys.path.append(HOME_DIR)
sys.path.append(os.path.join(HOME_DIR, "loader"))
sys.path.append(os.path.join(HOME_DIR, "RedBimEngine"))

clr.AddReference('System')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System.Web')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from common_scripts import *
from common_scripts.script_memory import SMemory
from common_scripts.form_creator import form_start

def say_plagin(plagin):
    plagin = urllib.quote(plagin.encode('utf8'), ':/')
    username = __revit__.Application.Username
    username = urllib.quote(username.encode('utf8'), ':/')
    url = "http://redbim.ru/plagin?plagin=" + plagin + "&username=" + username
    response = urllib.urlopen(url)

__file__ = FILE
file_path = os.path.dirname(FILE)
file_name = os.path.basename(file_path)
say_plagin(file_name)
FORM = form_start()
#
#
#
#
#