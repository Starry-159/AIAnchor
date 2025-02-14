import os
import sys
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QWidget, QFileDialog, QStatusBar, QComboBox
import soundfile as sf

from tools.i18n.i18n import I18nAuto
i18n = I18nAuto()

from inference_webui import gpt_path, sovits_path, change_gpt_weights, change_sovits_weights, get_tts_wav
 
from datetime import datetime
import os
import soundfile as sf


MODELS_PATH = "F:/AIAnchor/Input/GPT-SoVITS_Input/models"

"""
安装库
import subprocess
import sys

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# 示例：安装 requests 库
install_package("PyQt5")

"""


"""
类定义和初始化
class GPTSoVITSGUI(QMainWindow): 定义了一个继承自 QMainWindow 的类 GPTSoVITSGUI。QMainWindow 是 PyQt5 提供的主窗口类，通常用于创建主应用程序窗口。
"""
class GPTSoVITSGUI(QMainWindow):
    """
    self.GPT_Path 和 self.SoVITS_Path: 定义了两个实例变量，用于存储 GPT 和 SoVITS 模型的文件路径。初始化为空字符串。
    """
    GPT_Path = gpt_path
    SoVITS_Path = sovits_path

    def __init__(self):
        super().__init__()

        """
        self.setWindowTitle('GPT-SoVITS GUI'): 设置窗口标题为 "GPT-SoVITS GUI"。
        self.setGeometry(800, 450, 950, 850): 设置窗口的位置和大小。参数为 (x, y, width, height)，即窗口的左上角坐标和窗口的宽高。
        """
        self.setWindowTitle('GPT-SoVITS GUI')
        self.setGeometry(800, 450, 950, 850)

        """
        样式表设置
        self.setStyleSheet(...): 设置整个窗口及其控件的样式。
        QWidget: 设置所有 QWidget（包括子类如 QLabel 和 QPushButton）的背景色。
        QLabel: 设置所有 QLabel 的文字颜色。
        QPushButton: 设置所有 QPushButton 的背景色、文字颜色、内边距、边框和圆角。
        QPushButton:hover: 设置鼠标悬停时 QPushButton 的背景色、边框和阴影效果。
        """
        
        
        
        
        """
        QWidget
        背景色: 这个规则设置所有 QWidget 元素的背景色为 #87CEEB，即浅蓝色。通常 QWidget 是其他控件的基类，所以这个规则会影响所有的控件背景。
        QTabWidget::pane
        背景色: 这个规则设置 QTabWidget 的面板背景色为 #1e1e1e，即深灰色。这影响了选项卡控件的区域。
        QTabWidget::tab-bar
        对齐方式: 将选项卡栏（tab-bar）的对齐方式设置为左对齐。这会影响选项卡的排列位置。
        QTabBar::tab
        背景色: 选项卡的背景色设置为 #8da4bf，即淡蓝灰色。
        文字颜色: 文字颜色设置为白色 (#ffffff)。
        内边距: 选项卡的内边距设置为 8px，使得文本与选项卡的边缘保持一定距离。
        QTabBar::tab:selected
        选中的选项卡背景色: 选中状态下的选项卡背景色设置为 #2a3f54，即深青色，这样可以与其他选项卡区分开。
        QLabel
        文字颜色: QLabel 控件的文字颜色设置为黑色 (#000000)。
        QPushButton
        背景色: 按钮的背景色设置为 #ADD8E6，即浅蓝色。
        文字颜色: 文字颜色设置为白色 (white)。
        内边距: 按钮的内边距设置为 8px。
        边框: 边框设置为 1px 宽度的实线，颜色为 #003366，即深蓝色。
        圆角: 边框半径设置为 4px，使按钮有圆角效果。
        QPushButton:hover
        背景色: 鼠标悬停时，按钮的背景色更改为 #003366，即深蓝色。
        边框: 边框颜色在悬停状态下与背景色一致。
        阴影: 为按钮添加了 2px 的模糊阴影，使其在悬停时有轻微的浮起效果。
        """
        self.setStyleSheet("""
            QWidget {
                background-color: #87CEEB; 
            }

            QTabWidget::pane {
                background-color: #1e1e1e;  
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QTabBar::tab {
                background: #8da4bf; 
                color: #ffffff;  
                padding: 8px;
            }

            QTabBar::tab:selected {
                background: #2a3f54; 
            }

            QLabel {
                color: #000000;  
            }

            QPushButton {
                background-color: #ADD8E6; 
                color: white;  
                padding: 8px;
                border: 1px solid #003366;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #003366;  
                border: 1px solid #003366;
                box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
            }
        """)  


        """
        控件创建和布局
        license_text: 定义了一个字符串，包含软件的许可条款。
        license_label: 创建一个 QLabel 显示许可条款，并设置 setWordWrap(True) 使文字自动换行，以适应标签的宽度。
        """
        license_text = (
        "本软件以MIT协议开源, 作者不对软件具备任何控制力, 使用软件者、传播软件导出的声音者自负全责. "
        "如不认可该条款, 则不能使用或引用软件包内任何代码和文件. 详见根目录LICENSE.")
        license_label = QLabel(license_text)
        license_label.setWordWrap(True)

        """
        控件创建:
        self.GPT_model_label 和 self.SoVITS_model_label: 创建 QLabel 显示 "选择GPT模型:" 和 "选择SoVITS模型:" 的文本。
        self.GPT_model_input 和 self.SoVITS_model_input: 创建 QLineEdit 控件用于显示选择的文件路径，并设置占位符和只读属性。
        self.GPT_model_button 和 self.SoVITS_model_button: 创建 QPushButton 控件，用于选择 GPT 和 SoVITS 模型文件，并连接到相应的槽函数 select_GPT_model 和 select_SoVITS_model。
        QLabel: 标签控件，用于显示静态文本。
        QLineEdit: 单行文本输入框，设置为只读模式，用于显示选择的文件路径。
        QPushButton: 按钮控件，连接到相应的槽函数以执行操作。
        QComboBox: 下拉框控件，允许用户选择语言选项。
        QTextEdit: 多行文本编辑器，用于显示处理结果。
        信号连接:
        使用 clicked.connect 将按钮点击事件连接到相应的方法，如 select_ref_audio、upload_ref_text 等。
        """
        
        
        """
        QLabel
        功能: 用于显示固定文本“选择GPT模型:”，作为用户界面中的提示。
        用法: QLabel 是用于显示信息的控件，可以显示静态文本、图像或富文本。在这里，它作为提示标签，引导用户选择 GPT 模型。
        样式: 你可以通过 setStyleSheet 方法自定义标签的样式，例如字体、颜色等。
        """
        self.GPT_model_label = QLabel("选择GPT模型:")
        #创建一个文本输入框 (QLineEdit)，用于显示和管理文件路径。
        self.GPT_model_input = QLineEdit()
        #在文本框为空时显示的提示文本。在用户选择文件之前，显示“拖拽或选择文件”以指导用户操作。
        self.GPT_model_input.setPlaceholderText("拖拽或选择文件")
        #设置文本框的初始文本为 self.GPT_Path。self.GPT_Path 是一个字符串，通常包含文件的路径。这样，用户在选择文件之前，文本框会显示当前的文件路径（如果有的话）。
        self.GPT_model_input.setText(self.GPT_Path)
        #设置文本框为只读模式，这样用户不能直接编辑文本框中的内容。这通常用于显示信息而不允许修改。
        self.GPT_model_input.setReadOnly(True)
        """
        QPushButton
        创建一个按钮 (QPushButton)，当用户点击按钮时，将触发指定的操作。
        """
        #"选择GPT模型文件" 是按钮上显示的文本，明确告诉用户按钮的功能。
        self.GPT_model_button = QPushButton("选择GPT模型文件")
        #连接按钮的点击事件到 select_GPT_model 方法。connect 方法用于将信号（在这里是按钮的点击事件）与槽（即事件处理方法）连接。在按钮被点击时，会调用 select_GPT_model 方法处理文件选择逻辑。
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

        """
        创建一个下拉框 (QComboBox) 供用户选择参考音频语言，并设置默认值。
        """
        """
        #创建一个标签 (QLabel)，显示文本“参考音频语言:”，作为下拉框的描述。
        self.ref_language_label = QLabel("参考音频语言:")
        #创建一个下拉框控件 (QComboBox)，用于显示和选择语言选项。
        self.ref_language_combobox = QComboBox()
        #向下拉框中添加语言选项，包括“中文”、“英文”、“日文”等。
        self.ref_language_combobox.addItems(["中文", "英文", "日文", "中英混合", "日英混合", "多语种混合"])
        #设置下拉框的默认选项为“多语种混合”，确保界面在初始化时显示该选项。
        self.ref_language_combobox.setCurrentText("多语种混合")
        """


        # 创建并设置标签
        self.select_person_label = QLabel("选择人物：")
        # 创建下拉框
        self.select_person_combobox = QComboBox()
        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.select_person_label)
        layout.addWidget(self.select_person_combobox)
        self.setLayout(layout)
        # 扫描文件夹并更新下拉框
        self.update_person_options(MODELS_PATH)








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

        self.add_drag_drop_events([
            self.GPT_model_input,
            self.SoVITS_model_input,
            self.ref_audio_input,
            self.ref_text_input,
            self.target_text_input,
            self.output_input,
        ])

        self.synthesize_button = QPushButton("合成")
        self.synthesize_button.clicked.connect(self.synthesize)

        self.clear_output_button = QPushButton("清空输出")
        self.clear_output_button.clicked.connect(self.clear_output)

        self.status_bar = QStatusBar()

        """
        布局管理
        QVBoxLayout: 垂直布局管理器，用于管理窗口的主布局。
        QGridLayout: 网格布局管理器，用于组织输入控件，提供更精确的布局控制。
        QVBoxLayout (用于 output_layout): 将输出文本区域、合成按钮、清空按钮和状态栏添加到主布局中。
        """
        main_layout = QVBoxLayout()

        input_layout = QGridLayout(self)
        input_layout.setSpacing(10)

        input_layout.addWidget(license_label, 0, 0, 1, 3)

        input_layout.addWidget(self.GPT_model_label, 1, 0)
        input_layout.addWidget(self.GPT_model_input, 2, 0, 1, 2)
        input_layout.addWidget(self.GPT_model_button, 2, 2)

        input_layout.addWidget(self.SoVITS_model_label, 3, 0)
        input_layout.addWidget(self.SoVITS_model_input, 4, 0, 1, 2)
        input_layout.addWidget(self.SoVITS_model_button, 4, 2)

        input_layout.addWidget(self.ref_audio_label, 5, 0)
        input_layout.addWidget(self.ref_audio_input, 6, 0, 1, 2)
        input_layout.addWidget(self.ref_audio_button, 6, 2)


        """
        input_layout.addWidget(self.ref_language_label, 7, 0)
        input_layout.addWidget(self.ref_language_combobox, 8, 0, 1, 1)
        input_layout.addWidget(self.ref_text_label, 9, 0)
        input_layout.addWidget(self.ref_text_input, 10, 0, 1, 2)
        input_layout.addWidget(self.ref_text_button, 10, 2)
        """



        input_layout.addWidget(self.select_person_label, 7, 0)
        input_layout.addWidget(self.select_person_combobox, 8, 0, 1, 1)
        input_layout.addWidget(self.ref_text_label, 9, 0)
        input_layout.addWidget(self.ref_text_input, 10, 0, 1, 2)
        input_layout.addWidget(self.ref_text_button, 10, 2)

        input_layout.addWidget(self.target_language_label, 11, 0)
        input_layout.addWidget(self.target_language_combobox, 12, 0, 1, 1)
        input_layout.addWidget(self.target_text_label, 13, 0)
        input_layout.addWidget(self.target_text_input, 14, 0, 1, 2)
        input_layout.addWidget(self.target_text_button, 14, 2)

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

    """
    拖放事件处理
    dragEnterEvent: 处理拖拽进入事件，接受包含文件路径的拖拽。
    dropEvent: 处理拖拽释放事件，将拖拽的文件路径更新到相应的输入框。
    add_drag_drop_events: 为多个控件添加拖放支持。
    eventFilter: 事件过滤器，用于处理拖拽事件。
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
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

    """
    文件选择和上传
    使用 QFileDialog 打开文件选择对话框，让用户选择模型文件、音频文件、文本文件和输出文件夹。
    QFileDialog.getOpenFileName 用于选择单个文件，QFileDialog.getExistingDirectory 用于选择文件夹。
    """


    def update_person_options(self, directory):
        # 清空现有选项
        self.select_person_combobox.clear()
        
        try:
            # 获取指定目录中的所有子文件夹
            folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
            
            # 添加文件夹名称到下拉框
            self.select_person_combobox.addItems(folders)
            
            # 设置默认值（假设存在“多语种混合”文件夹，否则可以设置为第一个文件夹）
            if "多语种混合" in folders:
                self.select_person_combobox.setCurrentText("多语种混合")
            elif folders:
                self.select_person_combobox.setCurrentText(folders[0])  # 默认选择第一个文件夹
        except Exception as e:
            print(f"无法更新语言选项: {e}")


    def get_folder_path(self):
        selected_folder_name = self.select_person_combobox.currentText()
        if selected_folder_name:
            self.person_path = os.path.join(self.directory, selected_folder_name)
            print(f"选定文件夹的绝对路径是: {self.person_path}")
        else:
            print("未选择任何文件夹")



    def select_GPT_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择GPT模型文件", "", "GPT Files (*.ckpt)")
        if file_path:
            self.GPT_model_input.setText(file_path)

    def select_SoVITS_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择SoVITS模型文件", "", "SoVITS Files (*.pth)")
        if file_path:
            self.SoVITS_model_input.setText(file_path)

    def select_ref_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择参考音频文件", "", "Audio Files (*.wav *.mp3)")
        if file_path:
            self.update_ref_audio(file_path)

    def upload_ref_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.ref_text_input.setText(content)

    def upload_target_text(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.target_text_input.setText(content)

    def select_output_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly

        folder_dialog = QFileDialog()
        folder_dialog.setOptions(options)
        folder_dialog.setFileMode(QFileDialog.Directory)

        if folder_dialog.exec_():
            folder_path = folder_dialog.selectedFiles()[0]
            self.output_input.setText(folder_path)

    def update_ref_audio(self, file_path):
        self.ref_audio_input.setText(file_path)

    def clear_output(self):
        self.output_text.clear()

    """
    synthesize:
    读取各输入框的值。
    根据模型路径更新模型权重（通过 change_gpt_weights 和 change_sovits_weights）。
    调用 get_tts_wav 函数执行语音合成。
    保存生成的音频到指定路径。
    更新状态栏和输出文本区域显示合成结果。
    """
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
    mainWin = GPTSoVITSGUI()
    mainWin.show()
    sys.exit(app.exec_())