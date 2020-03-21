# -*- coding: utf-8 -*-
import os
import sys

RedBim_path = os.getenv('PROGRAMDATA')
revit_version = __revit__.Application.VersionNumber
RedBim_path = os.path.join(RedBim_path, "Autodesk", "Revit", "Addins", revit_version, "RedBim")
RedBim_loader_path = os.path.join(RedBim_path, "loader")

sys.path.append(RedBim_path)
sys.path.append(RedBim_loader_path)

from RedBimUpdater import RedBimUpdater
RedBimUpdater(RedBim_path)

# Запускаем движок
import RedBimEngine

RedBimEngine.find_all_tab()
