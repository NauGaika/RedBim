# -*- coding: utf-8 -*-
import clr, sys, os

HOME_DIR = os.getenv('PROGRAMDATA')
REVIT_VERSION = __revit__.Application.VersionNumber
HOME_DIR = os.path.join(HOME_DIR, "Autodesk", "Revit", "Addins", REVIT_VERSION, "RedBim")


sys.path.append(os.path.join(HOME_DIR, "loader"))
clr.AddReference('System')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System.Web')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
sys.path.append(HOME_DIR)

from common_scripts import *
from common_scripts.script_memory import SMemory
from common_scripts.form_creator import form_start

__file__ = FILE
file_path = os.path.dirname(FILE)
file_name = os.path.basename(file_path)
FORM = form_start()
#
#
#
#
#