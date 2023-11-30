from PyQt6.QtWidgets import QTreeWidgetItem


class DicomFileItem(QTreeWidgetItem):
    def __init__(self, path: str, *args, **kwargs):
        self.path = path
        file_name = path.split('/')[-1]
        self.visible_text = file_name
        super().__init__([file_name], *args, **kwargs)

    def get_path(self) -> str:
        return self.path


class DicomType(QTreeWidgetItem):
    def __init__(self, is_query: bool, *args, **kwargs):
        self.visible_text = 'Query File' if is_query else 'Supportive File'
        super().__init__([self.visible_text], *args, **kwargs)