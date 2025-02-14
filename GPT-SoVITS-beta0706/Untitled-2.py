import sys
import os
import soundfile as sf
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFileDialog, 
                             QStatusBar)
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt



from tools.i18n.i18n import I18nAuto
i18n = I18nAuto()

from inference_webui import gpt_path, sovits_path, change_gpt_weights, change_sovits_weights, get_tts_wav

from datetime import datetime
import os
import soundfile as sf

class GPTSoVITSGUI(QMainWindow):
    GPT_Path = gpt_path
    SoVITS_Path = sovits_path

    def __init__(self):
        super().__init__()
        self.setWindowTitle('GPT-SoVITS GUI')
        self.setGeometry(800, 450, 950, 850)

        self.init_ui()
        self.add_drag_drop_events([
            self.GPT_model_input,
            self.SoVITS_model_input,
            self.ref_audio_input,
            self.ref_text_input,
            self.target_text_input,
            self.output_input,
        ])

    def init_ui(self):

        layout = QVBoxLayout()

         # Widgets for file paths
        self.GPT_model_input = QLineEdit()
        self.SoVITS_model_input = QLineEdit()
        self.ref_audio_input = QLineEdit()
        self.ref_text_input = QLineEdit()
        

        self.select_person_folder1_label = QLabel("人物文件夹:")
        self.select_person_folder1_input = QLineEdit()
        self.select_person_folder1_input.setPlaceholderText("拖拽或选择文件")
        self.select_person_folder1.setText(self.GPT_Path)
        self.select_person_folder1.setReadOnly(True)
        self.select_person_folder1_button = QPushButton("选择人物文件夹")
        self.select_person_folder1_button.clicked.connect(self.select_GPT_model)


        #self.select_person_folder_btn = QPushButton("选择人物文件夹")





        self.select_color_folder_btn = QPushButton("选择音色文件夹")
        self.select_style_folder_btn = QPushButton("选择语气文件夹")
        self.default_mode_btn = QPushButton("默认模式")

        #self.select_person_folder_btn.clicked.connect(self.select_person_folder)
        self.select_color_folder_btn.clicked.connect(self.select_color_folder)
        self.select_style_folder_btn.clicked.connect(self.select_style_folder)
        self.default_mode_btn.clicked.connect(self.default_mode)



        # Initialize UI components
        self.GPT_model_label = QLabel("选择GPT模型:")
        self.GPT_model_input = QLineEdit()
        self.GPT_model_input.setPlaceholderText("拖拽或选择文件")
        self.GPT_model_input.setText(self.GPT_Path)
        self.GPT_model_input.setReadOnly(True)
        self.GPT_model_button = QPushButton("选择GPT模型文件")
        self.GPT_model_button.clicked.connect(self.select_GPT_model)

        self.SoVITS_model_label = QLabel("选择SoVITS模型:")
        self.SoVITS_model_input = QLineEdit()
        self.SoVITS_model_input.setPlaceholderText("拖拽或选择文件")
        self.SoVITS_model_input.setText(self.SoVITS_Path)
        self.SoVITS_model_input.setReadOnly(True)
        self.SoVITS_model_button = QPushButton("选择SoVITS模型文件")
        self.SoVITS_model_button.clicked.connect(self.select_SoVITS_model)

        self.ref_audio_label = QLabel("上传参考音频:")
        self.ref_audio_input = QLineEdit()
        self.ref_audio_input.setPlaceholderText("拖拽或选择文件")
        self.ref_audio_input.setReadOnly(True)
        self.ref_audio_button = QPushButton("选择音频文件")
        self.ref_audio_button.clicked.connect(self.select_ref_audio)

        self.ref_text_label = QLabel("参考音频文本:")
        self.ref_text_input = QLineEdit()
        self.ref_text_input.setPlaceholderText("直接输入文字或上传文本")
        self.ref_text_button = QPushButton("上传文本")
        self.ref_text_button.clicked.connect(self.upload_ref_text)

        self.ref_language_label = QLabel("参考音频语言:")
        self.ref_language_combobox = QComboBox()
        self.ref_language_combobox.addItems(["中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"])
        self.ref_language_combobox.setCurrentText("多语种混合")

        self.target_text_label = QLabel("合成目标文本:")
        self.target_text_input = QLineEdit()
        self.target_text_input.setPlaceholderText("直接输入文字或上传文本")
        self.target_text_button = QPushButton("上传文本")
        self.target_text_button.clicked.connect(self.upload_target_text)

        self.target_language_label = QLabel("合成音频语言:")
        self.target_language_combobox = QComboBox()
        self.target_language_combobox.addItems(["中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"])
        self.target_language_combobox.setCurrentText("多语种混合")

        self.output_label = QLabel("输出音频路径:")
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("拖拽或选择文件")
        self.output_input.setReadOnly(True)
        self.output_button = QPushButton("选择文件夹")
        self.output_button.clicked.connect(self.select_output_path)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.synthesize_button = QPushButton("合成")
        self.synthesize_button.clicked.connect(self.synthesize)

        self.clear_output_button = QPushButton("清空输出")
        self.clear_output_button.clicked.connect(self.clear_output)

        self.status_bar = QStatusBar()

        #self.setup_layout()


        main_layout = QVBoxLayout()

        input_layout = QGridLayout()
        input_layout.setSpacing(10)

        layout.addWidget(QLabel("GPT模型文件:"))
        layout.addWidget(self.GPT_model_input)
        layout.addWidget(QLabel("SoVITS模型文件:"))
        layout.addWidget(self.SoVITS_model_input)
        layout.addWidget(QLabel("参考音频文件:"))
        layout.addWidget(self.ref_audio_input)
        layout.addWidget(QLabel("参考文本文件:"))
        layout.addWidget(self.ref_text_input)

        input_layout.addWidget(self.select_person_folder_btn)
        input_layout.addWidget(self.select_color_folder_btn)
        input_layout.addWidget(self.select_style_folder_btn)
        input_layout.addWidget(self.default_mode_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        input_layout.addWidget(self.output_label, 15, 0)
        input_layout.addWidget(self.output_input, 16, 0, 1, 2)
        input_layout.addWidget(self.output_button, 16, 2)

        main_layout.addLayout(input_layout)

        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_text)
        main_layout.addLayout(output_layout)

        main_layout.addWidget(self.synthesize_button)
        main_layout.addWidget(self.clear_output_button)
        main_layout.addWidget(self.status_bar)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)


    def select_person_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择人物文件夹", "F:/AIAnchor/Input/GPT-SoVITS_Input/models")
        if folder_path:
            self.person_folder = folder_path
            self.select_color_folder()
    
    def select_color_folder(self):
        if not hasattr(self, 'person_folder'):
            QMessageBox.warning(self, "警告", "请先选择人物文件夹。")
            return

        folder_path = QFileDialog.getExistingDirectory(self, "选择音色文件夹", self.person_folder)
        if folder_path:
            self.color_folder = folder_path
            self.update_model_paths()

    def select_style_folder(self):
        if not hasattr(self, 'color_folder'):
            QMessageBox.warning(self, "警告", "请先选择音色文件夹。")
            return

        folder_path = QFileDialog.getExistingDirectory(self, "选择语气文件夹", self.color_folder)
        if folder_path:
            self.style_folder = folder_path
            self.update_file_paths()

    def default_mode(self):
        if not hasattr(self, 'person_folder'):
            QMessageBox.warning(self, "警告", "请先选择人物文件夹。")
            return

        # 自动选择音色文件夹
        color_folders = [os.path.join(self.person_folder, d) for d in os.listdir(self.person_folder) if os.path.isdir(os.path.join(self.person_folder, d))]
        if not color_folders:
            QMessageBox.warning(self, "警告", "人物文件夹中没有音色文件夹。")
            return
        
        self.color_folder = color_folders[0]

        # 自动选择语气文件夹
        style_folders = [os.path.join(self.color_folder, d) for d in os.listdir(self.color_folder) if os.path.isdir(os.path.join(self.color_folder, d))]
        if not style_folders:
            QMessageBox.warning(self, "警告", "音色文件夹中没有语气文件夹。")
            return

        self.style_folder = style_folders[0]

        self.update_model_paths()
        self.update_file_paths()

    def update_model_paths(self):
        if not hasattr(self, 'color_folder'):
            QMessageBox.warning(self, "警告", "音色文件夹未选择。")
            return

        files = os.listdir(self.color_folder)
        ckpt_files = [f for f in files if f.endswith('.ckpt')]
        pth_files = [f for f in files if f.endswith('.pth')]

        if ckpt_files:
            model_path = os.path.join(self.color_folder, ckpt_files[0])
            if self.GPT_model_input:
                print("Updating GPT_model_input")
                self.GPT_model_input.setText(model_path)
            else:
                print("self.GPT_model_input has been deleted or is None")

        if pth_files:
            model_path = os.path.join(self.color_folder, pth_files[0])
            if self.SoVITS_model_input:
                print("Updating SoVITS_model_input")
                self.SoVITS_model_input.setText(model_path)
            else:
                print("self.SoVITS_model_input has been deleted or is None")

    def update_file_paths(self):
        # 自动选择.wav和.txt文件
        files = os.listdir(self.style_folder)
        wav_files = [f for f in files if f.endswith('.wav')]
        txt_files = [f for f in files if f.endswith('.txt')]
        
        if wav_files:
            self.ref_audio_input.setText(os.path.join(self.style_folder, wav_files[0]))
        if txt_files:
            self.ref_text_input.setText(os.path.join(self.style_folder, txt_files[0]))


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            if len(file_paths) == 1:
                self.update_ref_audio(file_paths[0])
            else:
                self.update_ref_audio(", ".join(file_paths))

    def add_drag_drop_events(self, widgets):
        for widget in widgets:
            widget.setAcceptDrops(True)
            widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.DragEnter, QEvent.Drop):
            mime_data = event.mimeData()
            if mime_data.hasUrls():
                event.acceptProposedAction()
        return super().eventFilter(obj, event)

    def select_GPT_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择GPT模型文件", "", "模型文件 (*.ckpt);;所有文件 (*)")
        if file_path:
            self.GPT_model_input.setText(file_path)

    def select_SoVITS_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择SoVITS模型文件", "", "模型文件 (*.pth);;所有文件 (*)")
        if file_path:
            self.SoVITS_model_input.setText(file_path)

    def select_ref_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择音频文件", "", "音频文件 (*.wav *.mp3);;所有文件 (*)")
        if file_path:
            self.ref_audio_input.setText(file_path)

    def upload_ref_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "上传参考文本", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.ref_text_input.setText(file.read())

    def upload_target_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "上传目标文本", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.target_text_input.setText(file.read())

    def select_output_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.output_input.setText(folder_path)

    def synthesize(self):
        # Placeholder for synthesis logic
        self.output_text.append("合成中...")

    def clear_output(self):
        self.output_text.clear()

    def add_drag_drop_events(self, widgets):
        for widget in widgets:
            widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.DragEnter:
            if obj in [self.GPT_model_input, self.SoVITS_model_input, self.ref_audio_input, 
                       self.ref_text_input, self.target_text_input, self.output_input]:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True
        elif event.type() == QEvent.Drop:
            if obj in [self.GPT_model_input, self.SoVITS_model_input, self.ref_audio_input, 
                       self.ref_text_input, self.target_text_input, self.output_input]:
                file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
                if len(file_paths) == 1:
                    self.update_input_field(file_paths[0])
                event.acceptProposedAction()
                return True
        return super().eventFilter(obj, event)
    

    def synthesize(self):
        GPT_model_path = self.GPT_model_input.text()
        SoVITS_model_path = self.SoVITS_model_input.text()
        ref_audio_path = self.ref_audio_input.text()
        language_combobox = self.ref_language_combobox.currentText()
        language_combobox = i18n(language_combobox)
        ref_text = self.ref_text_input.text()
        target_language_combobox = self.target_language_combobox.currentText()
        target_language_combobox = i18n(target_language_combobox)
        target_text = self.target_text_input.text()
        output_path = self.output_input.text()

        if GPT_model_path != self.GPT_Path:
            change_gpt_weights(gpt_path=GPT_model_path)
            self.GPT_Path = GPT_model_path
        if SoVITS_model_path != self.SoVITS_Path:
            change_sovits_weights(sovits_path=SoVITS_model_path)
            self.SoVITS_Path = SoVITS_model_path

        synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path, 
                                       prompt_text=ref_text, 
                                       prompt_language=language_combobox, 
                                       text=target_text, 
                                       text_language=target_language_combobox)

        result_list = list(synthesis_result)


        # 获取当前时间并格式化
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join(output_path, current_time)

        # 创建目录
        os.makedirs(folder_path, exist_ok=True)

        #保存音频文件
        if result_list:
            last_sampling_rate, last_audio_data = result_list[-1]
            output_wav_path = os.path.join(folder_path, "output.wav") 
            sf.write(output_wav_path, last_audio_data, last_sampling_rate)

            result = "Audio saved to " + output_wav_path

        self.status_bar.showMessage("合成完成！输出路径：" + output_wav_path, 5000)
        self.output_text.append("处理结果：\n" + result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = GPTSoVITSGUI()
    main_win.show()
    sys.exit(app.exec_())