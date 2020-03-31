# coding: utf8

import re
import json
from Autodesk.Revit.UI import FileOpenDialog
from Autodesk.Revit.DB import Transaction, ModelPathUtils, WorksetTable, FilteredElementCollector, Workset, \
WorksetKind, FilteredWorksetCollector

doc = __revit__.ActiveUIDocument.Document


class RB_Workshared:
    def __init__(self, doc):
        self.doc = doc
        if self.is_workshared:
            if self.workset_file:
                self.workset_from_files = self.get_all_workset_for_file()
                self.worksets = [RB_Workset(i, self.doc) for i in self.workset_from_files]
            else:
                echo("Не выбран файл с рабочими наборами")
        else:
            echo("Включите совместную работу во вкладке Совместная работа")

    @property
    def is_workshared(self):
        return doc.IsWorkshared

    @property
    def workset_file(self):
        if not hasattr(self, "_workset_file"):
            dialog = FileOpenDialog("Файл с рабочими наборами json|*.json")
            dialog.Show()
            mpath = dialog.GetSelectedModelPath()
            if not mpath:
                self._workset_file = None
            else:
                self._workset_file = ModelPathUtils.ConvertModelPathToUserVisiblePath(mpath)
                with open(self._workset_file, 'rb') as f:
                    try:
                        self._workset_file = json.loads(f.read().decode("utf-8"))
                    except ValueError:
                        echo("Ошибка при разборе файла {}".format(self._workset_file))
                        self._workset_file = None
        return self._workset_file

    def get_all_workset_for_file(self):
        worksets = []
        for i in self.workset_file:
            template = i["template"]
            if template == "common":
                worksets += i['worksets']
            else:
                re_templ = re.compile(i["template"])
                if re_templ.search(self.doc.Title):
                    worksets += i['worksets']
        return worksets

    def create_workset(self):
        for i in self.worksets:
            RB_Workset(i, self.doc)


class RB_Workset:
    worksets = {}
    def __init__(self, workset, doc):
        self.doc = doc
        self.name = workset["name"]
        self.__class__.worksets[self.name] = self
        self.create_workset_if_not_exist()

    @property
    def all_exist_worksets(self):
        if not hasattr(self, "_all_exist_worksets"):
            self._all_exist_worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
            self._all_exist_worksets = {i.Name: i for i in self._all_exist_worksets}
        return self._all_exist_worksets

    def create_workset_if_not_exist(self):
        if WorksetTable.IsWorksetNameUnique(self.doc, self.name):
            self.workset = Workset.Create(self.doc, self.name)
            echo("Создан рабочий набор {}".format(self.name))
        else:
            self.workset = self.all_exist_worksets[self.name]

with Transaction(doc, 'Создание рабочих наборов') as t:
    t.Start()
    RB_Workshared(doc)
    t.Commit()
