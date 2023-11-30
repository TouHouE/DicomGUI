from PyQt6.QtWidgets import QMenu, QMenuBar, QFileDialog
from PyQt6.QtGui import QAction


class DeclaratorTopMenuBar(QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_menu = QMenu("File", self)
        # self.new_file_action = QAction("New File", self.file_menu)
        self.add_file_action = QAction("Add File", self.file_menu)
        self.open_folder_action = QAction("Open Folder", self.file_menu)

        # self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.add_file_action)
        self.file_menu.addAction(self.open_folder_action)

        self.addMenu(self.file_menu)


class TopMenuBar(DeclaratorTopMenuBar):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.add_file_action.triggered.connect(self.add_file)
        self.open_folder_action.triggered.connect(self.open_folder)

    def add_file(self):
        all_path, _ = QFileDialog.getOpenFileNames(filter='Dicom (*.dcm)')

        if len(all_path) == 0:
            return
        try:
            self.root.main_panel.tool_panel.add_list(all_path)
        except Exception as e:
            print(e)

    def open_folder(self):
        path = [QFileDialog.getExistingDirectory()]
        if len(path) == 0:
            return
        # main_panel = self.root.main_panel
        self.root.main_panel.tool_panel.update_list(path)
