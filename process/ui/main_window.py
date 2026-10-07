from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import sys

from ..main.rig_builder import fk_build_rig, ik_build_rig


def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QWidget) if ptr else None

class dynamic_ik_tab(QWidget):

    def __init__(self, key, joints, parent = None):
        super().__init__(parent)

        self.dynamic_ik_tab_text = QPlainTextEdit()
        self.dynamic_ik_tab_text.setPlaceholderText("Ik Joint list")
        self.dynamic_ik_tab_text.setFixedHeight(40)
        self.dynamic_ik_tab_text.setPlainText(f"{key} : {joints}")
        self.dynamic_ik_tab_text.setReadOnly(True)

        self.dynamic_ik_tab_layout = QVBoxLayout()
        self.dynamic_ik_tab_layout.addWidget(self.dynamic_ik_tab_text)
        self.setLayout(self.dynamic_ik_tab_layout)


class mbAutoRig_window(QMainWindow):
    def __init__(self, parent = None):

        if parent is None:
            parent = get_maya_main_window()

        super(mbAutoRig_window, self).__init__(parent)

        self.fk_rig_inst = fk_build_rig()
        self.ik_rig_inst = ik_build_rig()

        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.setWindowTitle('MB - Auto Rig')

        self.build_fk_rig_button = QPushButton("Build FK RIG")
        self.build_fk_rig_button.clicked.connect(self.fk_rig_inst.create_fk_rig)

        self.build_ik_rig_button = QPushButton("Build IK RIG")
        self.build_ik_rig_button.clicked.connect(self.ik_rig_inst.build_ik)

        self.add_ctrl_button = QPushButton("Joint list")
        self.add_ctrl_button.clicked.connect(self.show_joint_list)
        

        self.add_ik_button = QPushButton("Add IK")
        self.add_ik_button.clicked.connect(self.generate_dynamic_ik_tab)

        self.joint_field = QPlainTextEdit()
        self.joint_field.setPlaceholderText("Joint list")
        self.joint_field.setReadOnly(True)

        self.joint_ik_field = QPlainTextEdit()
        self.joint_ik_field.setPlaceholderText("Joint list")
        self.joint_ik_field.setReadOnly(True)

        self.ik_tabs = QVBoxLayout()

        self.executeTab = QHBoxLayout()
        self.executeTab.addWidget(self.build_fk_rig_button)
        self.executeTab.addWidget(self.build_ik_rig_button)
        
        self.button_stokage = QGridLayout()
        self.button_stokage.addWidget(self.add_ctrl_button, 1, 1)
        self.button_stokage.addWidget(self.add_ik_button, 1, 2)
        self.button_stokage.addWidget(self.joint_field, 2, 1)
        self.button_stokage.addLayout(self.ik_tabs, 2, 2)

        self.button_stokage.setColumnStretch(1, 1)
        self.button_stokage.setColumnStretch(2, 1)

        self.vertical_container = QVBoxLayout()
        self.vertical_container.addLayout(self.executeTab)
        self.vertical_container.addLayout(self.button_stokage)


        central_widget = QWidget()
        central_widget.setLayout(self.vertical_container)

        self.setCentralWidget(central_widget)


    def show_joint_list(self):
        joints = self.fk_rig_inst.retrieve_joint_list()
        self.joint_field.setPlainText("\n".join(f"Joint : {j}" for j in joints))


    def generate_dynamic_ik_tab(self):

        ik_log = self.ik_rig_inst.add_ik()     
        key, joints = list(ik_log.items())[-1]   

        ik_tab_instance = dynamic_ik_tab(key, joints, self)
        self.ik_tabs.addWidget(ik_tab_instance)



if __name__ == '__main__':
    app = QApplication(sys.argv)


    window = mbAutoRig_window()
    window.show()

    sys.exit(app.exec())