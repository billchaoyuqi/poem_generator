import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup, QPushButton, QTextEdit
)
from generator import Generator  # 请确保 Generator 类适应于 PyQt5 的使用


class PoetryGeneratorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互式诗歌生成器")
        self.generator = Generator()  # Generator 类需适应 PyQt5 的使用
        self.setFixedSize(800, 600)  # 固定窗口大小

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.keyword_entry = QLineEdit()
        form_layout.addRow("输入关键词:", self.keyword_entry)

        self.length_radio_5 = QRadioButton("五言")
        self.length_radio_7 = QRadioButton("七言")
        length_layout = QVBoxLayout()
        length_layout.addWidget(self.length_radio_5)
        length_layout.addWidget(self.length_radio_7)
        form_layout.addRow("诗的长度:", length_layout)

        self.labels_group = QButtonGroup()
        self.labels_group.setExclusive(False)
        self.label_options = [
            ("生活经历标签", ["军事生涯", "乡村生活", "其他"]),
            ("历史背景标签", ["繁荣时代", "动乱时代"]),
            ("是否存在量词", ["无", "有"]),
            ("是否存在顶针修辞", ["无", "有"]),
            ("是否存在天干地支", ["无", "有"])
        ]
        self.labels_buttons = []
        for label, options in self.label_options:
            label_widget = QLabel(label + ":")
            form_layout.addRow(label_widget)
            buttons_layout = QVBoxLayout()
            buttons_group = QButtonGroup()
            for idx, option in enumerate(options):
                button = QRadioButton(option)
                buttons_layout.addWidget(button)
                buttons_group.addButton(button, idx)
            form_layout.addRow(buttons_layout)
            self.labels_buttons.append(buttons_group)

        generate_button = QPushButton("生成诗歌")
        generate_button.clicked.connect(self.generate_poem)

        self.poem_output = QTextEdit()
        self.poem_output.setReadOnly(True)

        layout.addLayout(form_layout)
        layout.addWidget(generate_button)
        layout.addWidget(self.poem_output)

        self.setLayout(layout)

    def generate_poem(self):
        keyword = self.keyword_entry.text()
        length = 5 if self.length_radio_5.isChecked() else 7
        labels = []
        for button_group in self.labels_buttons:
            selected_id = button_group.checkedId()
            if selected_id != -1:
                labels.append(selected_id)

        if not keyword:
            self.poem_output.setText("请输入关键词")
            return

        try:
            lines, info = self.generator.generate_one(keyword, length, *labels, beam_size=20, verbose=1, manu=False)
            if lines:
                poem = "\n".join(lines)
                self.poem_output.setText(poem)
            else:
                self.poem_output.setText("生成失败：" + info)
        except Exception as e:
            self.poem_output.setText("生成失败：" + str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = PoetryGeneratorUI()
    ui.show()
    sys.exit(app.exec_())
