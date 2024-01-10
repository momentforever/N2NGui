from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarIcon, InfoBarPosition


class Info:
    @staticmethod
    def createErrorInfoBar(title="", content="", parent=None) -> InfoBar:
        return InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5 * 1000,    # won't disappear automatically
            parent=parent
        )
