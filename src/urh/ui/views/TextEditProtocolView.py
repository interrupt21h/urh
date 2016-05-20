
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QContextMenuEvent, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QApplication, QMenu, QActionGroup


class TextEditProtocolView(QPlainTextEdit):
    proto_view_changed = pyqtSignal()
    deletion_wanted = pyqtSignal()
    show_proto_clicked = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)
        self.cur_view = 0
        self.participants = None
        """:type: list of Participant """

        self.blocks = None
        """:type: list of ProtocolBlock """

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.deletion_wanted.emit()
        super().keyPressEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent):
        QApplication.processEvents()
        menu = QMenu(self)
        viewgroup = QActionGroup(self)
        viewmenu = menu.addMenu("View")
        bitAction = viewmenu.addAction("Bits")
        bitAction.setCheckable(True)
        hexAction = viewmenu.addAction("Hex")
        hexAction.setCheckable(True)
        asciiAction = viewmenu.addAction("ASCII")
        asciiAction.setCheckable(True)

        menu.addSeparator()

        if self.participants:# and self.blocks:
            partigroup = QActionGroup(self)
            participant_menu = menu.addMenu("Participant")
            none_partipnt_action = participant_menu.addAction("None")
            none_partipnt_action.setCheckable(True)
            none_partipnt_action.setActionGroup(partigroup)
            for particpnt in self.participants:
                pa = participant_menu.addAction(particpnt.name + " (" + particpnt.shortname + ")")
                pa.setCheckable(True)
                pa.setActionGroup(partigroup)


        show_proto_action = menu.addAction("Zoom to bits in signal")

        menu.addSeparator()

        linewrapAction = menu.addAction("Linewrap (may take a while for long protocols)")
        linewrapAction.setCheckable(True)

        linewrap = self.lineWrapMode() == QPlainTextEdit.WidgetWidth

        linewrapAction.setChecked(linewrap)

        sel_text = self.textCursor().selectedText().replace("\n", "")

        bitAction.setActionGroup(viewgroup)
        hexAction.setActionGroup(viewgroup)
        asciiAction.setActionGroup(viewgroup)

        if self.cur_view == 0:
            bitAction.setChecked(True)
        elif self.cur_view == 1:
            hexAction.setChecked(True)
        elif self.cur_view == 2:
            asciiAction.setChecked(True)

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action is None:
            return
        elif action == bitAction:
            self.cur_view = 0
            self.proto_view_changed.emit()
        elif action == hexAction:
            self.cur_view = 1
            self.proto_view_changed.emit()
        elif action == asciiAction:
            self.cur_view = 2
            self.proto_view_changed.emit()
        elif action == linewrapAction:
            linewrap = linewrapAction.isChecked()

            if linewrap:
                self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
            else:
                self.setLineWrapMode(QPlainTextEdit.NoWrap)
        elif action == show_proto_action:
            self.show_proto_clicked.emit()

    def textCursor(self) -> QTextCursor:
        return super().textCursor()
