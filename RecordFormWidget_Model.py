from PyQt5.QtWidgets import QWidget

from RecordFormWidget_UI import Record_Ui_Form


class RecordFormWidget(QWidget, Record_Ui_Form):
    def __init__(self, parent=None):
        super(RecordFormWidget, self).__init__(parent)
        self.setupUi(self)