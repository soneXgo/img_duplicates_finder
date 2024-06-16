from PyQt5.QtWidgets import QDialog, QFormLayout, QCheckBox, QDialogButtonBox, QVBoxLayout, \
    QFrame, QLabel, QSpacerItem, QSizePolicy, QComboBox, QScrollArea, QWidget
from PyQt5.QtGui import QFont


class OptionsDialog(QDialog):
    def __init__(self, options, parent=None):
        super().__init__(parent)

        self.setWindowTitle("General options")
        self.setFont(QFont("OpenSans", 10))
        self.options = options

        dlg_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(560, 400)
        self.scroll_widget = QWidget()
        self.form_layout = QFormLayout(self.scroll_widget)
        self.form_layout.setHorizontalSpacing(32)
        self.form_layout.addRow(QLabel("<h3>General options</h3>"))

        self.add_separator("<b>When searching for duplicates</b>")
        self.create_folder_options()
        self.search_by_options()
        self.create_algorithm_options()
        self.add_separator("<b>Image properties</b>")
        self.create_image_property_options()

        self.scroll_area.setWidget(self.scroll_widget)
        dlg_layout.addWidget(self.scroll_area)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        dlg_layout.addWidget(buttons)

    def create_folder_options(self):
        self.folder_combo = QComboBox()
        self.folder_combo.setMaximumWidth(200)
        self.folder_combo.addItems(["Recursive Search", "In the Current Folder"])

        if self.options.get("recursive_search"):
            self.folder_combo.setCurrentIndex(0)
        else:
            self.folder_combo.setCurrentIndex(1)

        self.form_layout.addRow("Folders for search:", self.folder_combo)

    def search_by_options(self):
        self.search_by_combo = QComboBox()
        self.search_by_combo.setMaximumWidth(200)
        self.search_by_combo.addItems(["Content", "Name", "Size"])

        selected_search_by = self.options.get("search_by")
        if selected_search_by == "Content":
            self.search_by_combo.setCurrentIndex(0)
        elif selected_search_by == "Name":
            self.search_by_combo.setCurrentIndex(1)
        elif selected_search_by == "Size":
            self.search_by_combo.setCurrentIndex(2)

        self.form_layout.addRow("Search by:", self.search_by_combo)

    def create_algorithm_options(self):
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.setMaximumWidth(200)
        self.algorithm_combo.addItems(["aHash", "pHash", "ORB"])

        selected_algorithm = self.options.get("algorithm")
        if selected_algorithm == "aHash":
            self.algorithm_combo.setCurrentIndex(0)
        elif selected_algorithm == "pHash":
            self.algorithm_combo.setCurrentIndex(1)
        elif selected_algorithm == "ORB":
            self.algorithm_combo.setCurrentIndex(2)

        self.form_layout.addRow("Algorithm:", self.algorithm_combo)

    def create_image_property_options(self):
        self.limit_size = QCheckBox("Limit Size")
        self.limit_creation_date = QCheckBox("Limit Creation Date")
        self.limit_changing_date = QCheckBox("Limit Changing Date")

        self.form_layout.addRow(self.limit_size)
        self.form_layout.addRow(self.limit_creation_date)
        self.form_layout.addRow(self.limit_changing_date)

        self.limit_size.setChecked(self.options.get("limit_size", False))
        self.limit_creation_date.setChecked(self.options.get("limit_creation_date", False))
        self.limit_changing_date.setChecked(self.options.get("limit_changing_date", False))

    def get_options(self):
        return {
            "recursive_search": self.folder_combo.currentIndex() == 0,
            "search_by": self.search_by_combo.currentText(),
            "algorithm": self.algorithm_combo.currentText(),
            "limit_size": self.limit_size.isChecked(),
            "limit_creation_date": self.limit_creation_date.isChecked(),
            "limit_changing_date": self.limit_changing_date.isChecked()
        }

    def add_separator(self, text):
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.form_layout.addItem(spacer)
        self.form_layout.addRow(QLabel(text))
        self.form_layout.addRow(separator)
