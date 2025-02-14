import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QComboBox, 
                             QVBoxLayout, QWidget, QPushButton, QFileDialog)

class FolderSelector(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.person_path = ""
        self.voice_path = ""
        self.motion_path = ""

        # 设置窗口
        self.setWindowTitle("Folder Selector")
        self.setGeometry(100, 100, 600, 400)

        # 创建部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        """
        # 创建标签和下拉框
        self.ref_language_label = QLabel("参考音频语言:")
        self.ref_language_combobox = QComboBox()
        self.layout.addWidget(self.ref_language_label)
        self.layout.addWidget(self.ref_language_combobox)
        """

        # 创建下拉框
        self.person_combobox = QComboBox()
        self.voice_combobox = QComboBox()
        self.motion_combobox = QComboBox()
        self.layout.addWidget(QLabel("Person Path:"))
        self.layout.addWidget(self.person_combobox)
        self.layout.addWidget(QLabel("Voice Path:"))
        self.layout.addWidget(self.voice_combobox)
        self.layout.addWidget(QLabel("Motion Path:"))
        self.layout.addWidget(self.motion_combobox)

        # 创建按钮
        self.choose_folder_button = QPushButton("选择根文件夹")
        self.layout.addWidget(self.choose_folder_button)

        # 连接信号
        self.choose_folder_button.clicked.connect(self.select_root_folder)
        self.person_combobox.currentIndexChanged.connect(self.update_voice_combobox)
        self.voice_combobox.currentIndexChanged.connect(self.update_motion_combobox)

        # 初始化
        self.root_folder = "F:\\AIAnchor\\Input\\GPT-SoVITS_Input\\models"
        self.update_person_combobox()

    def select_root_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择根文件夹", self.root_folder)
        if folder_path:
            self.root_folder = folder_path
            self.update_person_combobox()

    def update_person_combobox(self):
        self.person_combobox.clear()
        if os.path.exists(self.root_folder):
            subfolders = [f for f in os.listdir(self.root_folder) if os.path.isdir(os.path.join(self.root_folder, f))]
            self.person_combobox.addItems(subfolders)

    def update_voice_combobox(self):
        selected_person_folder = self.person_combobox.currentText()
        if selected_person_folder:
            self.person_path = os.path.join(self.root_folder, selected_person_folder)
            self.voice_combobox.clear()
            if os.path.exists(self.person_path):
                subfolders = [f for f in os.listdir(self.person_path) if os.path.isdir(os.path.join(self.person_path, f))]
                self.voice_combobox.addItems(subfolders)

    def update_motion_combobox(self):
        selected_voice_folder = self.voice_combobox.currentText()
        if selected_voice_folder:
            self.voice_path = os.path.join(self.person_path, selected_voice_folder)
            self.motion_combobox.clear()
            if os.path.exists(self.voice_path):
                subfolders = [f for f in os.listdir(self.voice_path) if os.path.isdir(os.path.join(self.voice_path, f))]
                self.motion_combobox.addItems(subfolders)

    def get_paths(self):
        self.motion_path = os.path.join(self.voice_path, self.motion_combobox.currentText())
        return self.person_path, self.voice_path, self.motion_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderSelector()
    window.show()
    sys.exit(app.exec_())
