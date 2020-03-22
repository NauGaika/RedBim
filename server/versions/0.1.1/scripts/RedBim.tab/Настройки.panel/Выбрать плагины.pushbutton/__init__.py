# -*- coding: utf-8 -*-
"""Модуль который ищет вкладки. Здесь функция find_all_tab."""

import os
import re

from constants import DIR_SCRIPTS, STATIC_IMAGE, HOME_DIR  # Подгружаем общие переменные

import os
import json
from System.Windows.Forms import MessageBox, Application, Form, DockStyle, BorderStyle, TextBox, ScrollBars, AnchorStyles, AutoScaleMode
from System.Windows.Forms import ImageLayout, FormStartPosition, Label, TreeView, Button
from System.Windows.Forms import TreeNode, TreeViewAction
from System.Web.UI.WebControls import TreeNodeTypes
from System.Drawing import Font, FontStyle, Color, Point, Image, Icon

class RB_TreeView(TreeView):
    def __init__(self):
        self.AfterCheck += self.node_AfterCheck

    def node_AfterCheck(self, sender, e):
        if e.Action != TreeViewAction.Unknown:
            self.CheckAllParentNodes(e.Node, e.Node.Checked)
            if e.Node.Nodes.Count > 0:
                self.CheckAllChildNodes(e.Node, e.Node.Checked)

    def CheckAllChildNodes(self,treeNode, nodeChecked):
        
        for node in treeNode.Nodes:
            node.Checked = nodeChecked
            if node.Nodes.Count > 0:
                self.CheckAllChildNodes(node, nodeChecked)

    def CheckAllParentNodes(self, treeNode, nodeChecked):
        if hasattr(treeNode, "Parent"):
            if treeNode.Parent:
                if nodeChecked:
                    treeNode.Parent.Checked = nodeChecked
                    self.CheckAllParentNodes(treeNode.Parent, nodeChecked)

class RedBimSetting(Form):
    def __init__(self):
        self.pushbutons = []

        self.Text = 'RedBim набор плагинов'
        self.Name = 'RedBimSetting'
        self.Height = 450
        self.Width = 400
        self.AutoScroll = True
        self.AutoScaleMode = AutoScaleMode.Font
        self.BackColor = Color.FromArgb(67, 67, 67)
        self.BackgroundImage = Image.FromFile(os.path.join(STATIC_IMAGE, "bg.png"))
        self.BackgroundImageLayout = ImageLayout.Center
        self.Icon = Icon(os.path.join(STATIC_IMAGE, "icon.ico"), 16, 16)
        self.StartPosition = FormStartPosition.CenterScreen
        self.tree = RB_TreeView()
        self.tree.CollapseAll()
        self.tree.BackColor = Color.FromArgb(67, 67, 67)
        self.tree.BackgroundImage = Image.FromFile(os.path.join(STATIC_IMAGE, "bg.png"))
        self.tree.BackgroundImageLayout = ImageLayout.Center
        self.tree.Font = Font("ISOCPEUR", 12, FontStyle.Italic)
        self.tree.ForeColor = Color.White
        self.tree.CheckBoxes = True
        self.tree.Height = 378
        self.tree.Dock = DockStyle.Top
        self.find_all_pushbuttons()
        self.button = Button()
        self.button.Dock = DockStyle.Bottom
        self.button.Text = "Сохранить настройки"
        self.button.Height = 32
        self.button.Font = Font("ISOCPEUR", 12, FontStyle.Italic)
        self.button.ForeColor = Color.White
        self.button.BackColor = Color.Green
        self.button.Click += self.active_button
        self.Controls.Add(self.button)
        self.Controls.Add(self.tree)

    def find_element(self, path, element, parent=None):
        ress = []
        for i in os.listdir(path):
            if i[len(element) * -1:] == element:
                result = {}
                result.setdefault("path", os.path.join(path, i))
                result.setdefault("element_type", element[1:])
                result.setdefault("name", i)
                result.setdefault("parent", parent)
                ress.append(result)
        return ress

    def checked_elements(self, element, obj=None):
        if element.Nodes.Count > 0:
            for node in element.Nodes:
                res = {}
                res.setdefault("active", node.Checked)
                res.setdefault("name", node.Text)
                res.setdefault("childs", [])
                if node.Nodes.Count > 0:
                    self.checked_elements(node, obj=res["childs"])
                obj.append(res)


    def active_button(self, sender, e):
        res = []
        self.checked_elements(self.tree, obj=res)
        config_path = os.path.join(HOME_DIR, "config.json")
        with open(config_path, "w") as f:
            json.dump(res, f)
            f.close()
        message("Плагины изменяться при перезапуске Revit")
        self.Close()




    def find_all_pushbuttons(self):
        tabs = self.find_element(DIR_SCRIPTS, ".tab")
        for i in tabs:
            i.setdefault("node", TreeNode())
            i["node"].Text = i["name"]
            self.tree.Nodes.Add(i["node"])
            panels = self.find_element(i["path"], ".panel", parent=i)
            for panel in panels:
                panel.setdefault("node", TreeNode())
                panel["node"].Text = panel["name"]
                i["node"].Nodes.Add(panel["node"])
                pbs = self.find_element(panel["path"], ".pushbutton", parent=panel)
                for pb in pbs:
                    pb.setdefault("node", TreeNode())
                    pb["node"].Text = pb["name"]
                    panel["node"].Nodes.Add(pb["node"])

form = RedBimSetting()
form.Show()