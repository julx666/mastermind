import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to the Mastermind game")
        # self.setGeometry(x, y, width, height)
        self.setGeometry(350, 100, 700, 700)
        self.initUI()

        label = QLabel("Hello", self)
        label.setFont(QFont("Arial", 15))
        label.setStyleSheet("color: #64cbd9;"
                            "font-weight: bold;")
        label.move(300, 0)

        # label.setAlignment(Qt.AlignTop) # vertically top
        # label.setAlignment(Qt.AlignBottom) # vertically bottom
        # label.setAlignment(Qt.AlignVCenter) # vertically center

        # label.setAlignment(Qt.AlignRight)  # horizontally right
        # label.setAlignment(Qt.AlignLeft)  # horizontally left
        # label.setAlignment(Qt.AlignHCenter)  # horizontally center

        label.setAlignment(Qt.AlignCenter)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawRect(150, 70, 400, 600)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
