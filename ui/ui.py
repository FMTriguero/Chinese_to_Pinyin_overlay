from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, Qt, QObject, Signal
from PySide2.QtGui import QSurfaceFormat, QSurface, QColor, QFont


class UIBackend(QObject):
    onOverlayInfoAdded = Signal("QVariant")
    onOverlayInfoCleared = Signal()


class UI:

    def __init__(self):
        self.toggle_input_transparency = True
        self.backend = UIBackend()
        self.infos = []
        self.app = QApplication([])
        self.view = None

    def initialize(self):
        print("Initializing ui")

        view = QQuickView()
        view.rootContext().setContextProperty("backend", self.backend)

        view.setFlags(view.flags() | Qt.WindowStaysOnTopHint)
        view.setSurfaceType(QSurface.OpenGLSurface)

        surface_format = QSurfaceFormat()
        surface_format.setDepthBufferSize(1)
        surface_format.setAlphaBufferSize(8)
        surface_format.setRenderableType(QSurfaceFormat.OpenGL)

        view.setFormat(surface_format)
        view.setColor(QColor(Qt.transparent))
        view.setClearBeforeRendering(True)

        view.setSource(QUrl("ui/overlay/overlay.qml"))

        view.show()

        self.app.setFont(QFont("Times", 10))

        self.view = view

        return self.app.exec_()

    def reset(self):
        self.backend.onOverlayInfoCleared.emit()
        self.infos.clear()

        if self.toggle_input_transparency:
            self.view.setFlags(self.view.flags() | Qt.WindowTransparentForInput)

    def add_text(self, position, text, tooltip):
        info = {
            "position": list(position),
            "text": text,
            "tooltip": tooltip
        }

        if self.toggle_input_transparency:
            self.view.setFlags(self.view.flags() & ~Qt.WindowTransparentForInput)

        self.infos.append(info)

        self.backend.onOverlayInfoAdded.emit(info)

    def get_monitor_coordinates(self):
        return {
            "left": self.view.x(),
            "top": self.view.y(),
            "width": self.view.width(),
            "height": self.view.height()
        }
