from pathlib import Path

import mammoth
from markdownify import markdownify as md
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DocToMarkdown(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Word to Markdown Converter")

        # Layout
        layout = QVBoxLayout()

        # Label and input for .docx file
        self.docx_label = QLabel("Select .doc files:")
        layout.addWidget(self.docx_label)
        self.docx_input = QTextEdit(self)
        layout.addWidget(self.docx_input)
        self.docx_button = QPushButton("Browse", self)
        self.docx_button.clicked.connect(self.select_docx_file)
        layout.addWidget(self.docx_button)

        # Label and input for .md file
        self.md_label = QLabel("Select the save path:")
        layout.addWidget(self.md_label)
        self.md_input = QLineEdit(self)
        layout.addWidget(self.md_input)
        self.md_button = QPushButton("Browse", self)
        self.md_button.clicked.connect(self.select_md_save_path)
        layout.addWidget(self.md_button)

        # Convert button
        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)

        # Set layout
        self.setLayout(layout)

    # Function to select .docx file
    def select_docx_file(self):
        options = QFileDialog.Options()
        self.input_docs, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Word Document",
            "/home/noah/Documents/rag_test/contract/",
            "Word Files (*.docx)",
            options=options,
        )
        if self.input_docs:
            for name in self.input_docs:
                self.docx_input.append(Path(name).name)

    def select_md_save_path(self):
        options = QFileDialog.Options()
        save_path = QFileDialog.getExistingDirectory(
            self, "Select Save Directory", "", options=options
        )
        if save_path:
            self.md_input.setText(save_path)

    # Convert function
    def convert(self):
        try:
            for doc in self.input_docs:
                save_md = Path(
                    self.md_input.text(),
                    Path(Path(doc).stem).with_suffix(".md").as_posix(),
                )
                with open(doc, "rb") as input_doc:
                    result = mammoth.convert_to_html(input_doc)
                    html = result.value
                    with open(save_md, "w") as output_md:
                        output_md.write(md(html))

            QMessageBox.information(
                self, "Success", f"Markdown file(s) saved at: {self.md_input.text()}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# Main function to start the application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    converter = DocToMarkdown()
    converter.resize(400, 200)
    converter.show()
    sys.exit(app.exec_())
