import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QMessageBox
)
from generator import Generator  # 请确保 Generator 类适应于 PyQt5 的使用

class PoetryGeneratorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互式诗歌生成器")
        self.generator = Generator()  # Generator 类需适应 PyQt5 的使用

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.keyword_entry = QLineEdit()
        form_layout.addRow("输入关键词:", self.keyword_entry)

        self.length_radio_5 = QRadioButton("五言")
        self.length_radio_7 = QRadioButton("七言")
        length_layout = QHBoxLayout()
        length_layout.addWidget(self.length_radio_5)
        length_layout.addWidget(self.length_radio_7)
        form_layout.addRow("诗的长度:", length_layout)

        self.labels_entries = []
        labels_descriptions = [
            "生活经历标签 (0: 军事生涯, 1: 乡村生活, 2: 其他, -1: 不指定)",
            "历史背景标签 (0: 繁荣时代, 1: 动乱时代, -1: 不指定)",
            "是否存在量词 (0: 无, 1: 有, -1: 不指定)",
            "是否存在顶针修辞 (0: 无, 1: 有, -1: 不指定)",
            "是否存在天干地支 (0: 无, 1: 有, -1: 不指定)"
        ]
        for label in labels_descriptions:
            entry = QLineEdit()
            self.labels_entries.append(entry)
            form_layout.addRow(label, entry)

        generate_button = QPushButton("生成诗歌")
        generate_button.clicked.connect(self.generate_poem)
        layout.addLayout(form_layout)
        layout.addWidget(generate_button)

        self.setLayout(layout)

    def generate_poem(self):
        keyword = self.keyword_entry.text()
        length = 5 if self.length_radio_5.isChecked() else 7
        labels = [int(entry.text()) if entry.text().isdigit() else -1 for entry in self.labels_entries]

        if not keyword:
            QMessageBox.critical(self, "错误", "请输入关键词")
            return

        try:
            lines, info = self.generator.generate_one(keyword, length, *labels, beam_size=20, verbose=1, manu=False)
            if lines:
                QMessageBox.information(self, "生成的诗歌", "\n".join(lines))
            else:
                QMessageBox.critical(self, "错误", "生成失败：" + info)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = PoetryGeneratorUI()
    ui.show()
    sys.exit(app.exec_())
