from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QGridLayout, QSpinBox, QRadioButton,
                           QButtonGroup, QMessageBox, QInputDialog)
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QSize, QTimer
import sys
from judge import Judge
from player import AutoPlayer, ManualPlayer

class PegWidget(QWidget):
    def __init__(self, color=Qt.gray, size=30):
        super().__init__()
        self.color = color
        self.setFixedSize(QSize(size, size))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(2, 2, self.width()-4, self.height()-4)
        
    def setColor(self, color):
        self.color = color
        self.update()

class MastermindBoard(QWidget):
    COLORS = [QColor(Qt.red), QColor(Qt.blue), QColor(Qt.green), 
              QColor(Qt.yellow), QColor(Qt.cyan), QColor(Qt.magenta)]
    
    def __init__(self, k, n, is_auto_mode=False):
        super().__init__()
        self.k = k
        self.n = n
        self.current_row = 0
        self.current_col = 0
        self.is_auto_mode = is_auto_mode
        self.initUI()
        
    def initUI(self):
        layout = QGridLayout()
        self.pegs = []
        self.feedback_pegs = []
        
        # Create game board
        for row in range(self.n):
            row_pegs = []
            row_feedback = []
            
            # Main pegs
            for col in range(self.k):
                peg = PegWidget(QColor(Qt.gray))
                layout.addWidget(peg, row, col)
                row_pegs.append(peg)
                
            # Feedback pegs
            feedback_widget = QWidget()
            feedback_layout = QGridLayout()
            for i in range(2):
                for j in range(2):
                    feedback_peg = PegWidget(QColor(Qt.gray), size=15)
                    feedback_layout.addWidget(feedback_peg, i, j)
                    row_feedback.append(feedback_peg)
            
            feedback_widget.setLayout(feedback_layout)
            layout.addWidget(feedback_widget, row, self.k)
            
            self.pegs.append(row_pegs)
            self.feedback_pegs.append(row_feedback)
        
        # Only show color selection and submit button in manual mode
        if not self.is_auto_mode:
            # Color selection
            color_widget = QWidget()
            color_layout = QHBoxLayout()
            for i, color in enumerate(self.COLORS[:self.k]):
                color_button = QPushButton()
                color_button.setFixedSize(QSize(30, 30))
                color_button.setStyleSheet(f"background-color: {color.name()}")
                color_button.clicked.connect(lambda checked, c=color: self.selectColor(c))
                color_layout.addWidget(color_button)
            
            color_widget.setLayout(color_layout)
            layout.addWidget(color_widget, self.n, 0, 1, self.k)
            
            # Submit button
            self.submit_button = QPushButton("Submit")
            layout.addWidget(self.submit_button, self.n, self.k)
        else:
            # Auto play button
            self.auto_play_button = QPushButton("Make Auto Move")
            layout.addWidget(self.auto_play_button, self.n, 0, 1, self.k + 1)
        
        self.setLayout(layout)
        
    def selectColor(self, color):
        if self.current_row < self.n and self.current_col < self.k:
            self.pegs[self.current_row][self.current_col].setColor(color)
            self.current_col = (self.current_col + 1) % self.k
            
    def getCurrentGuess(self):
        guess = []
        for peg in self.pegs[self.current_row]:
            color = peg.color
            if color == QColor(Qt.gray):
                return None
            guess.append(self.COLORS.index(color) + 1)
        return guess
    
    def setGuess(self, guess):
        for i, num in enumerate(guess):
            self.pegs[self.current_row][i].setColor(self.COLORS[num - 1])
        self.current_col = self.k
    
    def updateFeedback(self, exact, color):
        feedback_row = self.feedback_pegs[self.current_row]
        idx = 0
        
        for _ in range(exact):
            feedback_row[idx].setColor(QColor(Qt.black))
            idx += 1
            
        for _ in range(color):
            feedback_row[idx].setColor(QColor(Qt.white))
            idx += 1

class MastermindGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGame()
        self.initUI()
        
    def initGame(self):
        self.k = 4
        self.n = 10
        self.judge = Judge()
        self.hidden_seq = None
        self.game_over = False
        self.auto_player = None
        
    def initUI(self):
        self.setWindowTitle("Mastermind")
        self.setGeometry(100, 100, 600, 800)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Game configuration
        config_layout = QHBoxLayout()
        
        # K selection
        k_layout = QVBoxLayout()
        k_label = QLabel("Colors (K):")
        self.k_spin = QSpinBox()
        self.k_spin.setRange(1, 6)
        self.k_spin.setValue(self.k)
        k_layout.addWidget(k_label)
        k_layout.addWidget(self.k_spin)
        config_layout.addLayout(k_layout)
        
        # N selection
        n_layout = QVBoxLayout()
        n_label = QLabel("Attempts (N):")
        self.n_spin = QSpinBox()
        self.n_spin.setRange(1, 20)
        self.n_spin.setValue(self.n)
        n_layout.addWidget(n_label)
        n_layout.addWidget(self.n_spin)
        config_layout.addLayout(n_layout)
        
        # Game mode selection
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Game Mode:")
        self.auto_radio = QRadioButton("Auto Player")
        self.manual_radio = QRadioButton("Manual Player")
        self.manual_radio.setChecked(True)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.auto_radio)
        mode_layout.addWidget(self.manual_radio)
        config_layout.addLayout(mode_layout)

        # Sequence selection
        seq_layout = QVBoxLayout()
        seq_label = QLabel("Hidden Sequence:")
        self.random_seq_radio = QRadioButton("Random")
        self.manual_seq_radio = QRadioButton("Manual")
        self.random_seq_radio.setChecked(True)
        seq_layout.addWidget(seq_label)
        seq_layout.addWidget(self.random_seq_radio)
        seq_layout.addWidget(self.manual_seq_radio)
        config_layout.addLayout(seq_layout)
        
        # Start button
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.startGame)
        config_layout.addWidget(self.start_button)
        
        layout.addLayout(config_layout)
        
        # Placeholder for the game board
        self.board_widget = QWidget()
        layout.addWidget(self.board_widget)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def getManualSequence(self):
        sequence = []
        valid_input = False
        
        while not valid_input:
            text, ok = QInputDialog.getText(
                self, 
                'Enter Hidden Sequence',
                f'Enter {self.k} numbers (1-{self.k}) separated by commas:'
            )
            
            if not ok:
                return None
                
            try:
                sequence = [int(x.strip()) for x in text.split(',')]
                if len(sequence) != self.k or not all(1 <= x <= self.k for x in sequence):
                    QMessageBox.warning(self, "Invalid Input", 
                        f"Please enter exactly {self.k} numbers between 1 and {self.k}")
                    continue
                valid_input = True
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers")
                
        return sequence
        
    def startGame(self):
        self.k = self.k_spin.value()
        self.n = self.n_spin.value()
        self.game_over = False
        
        # Get hidden sequence
        if self.manual_seq_radio.isChecked():
            self.hidden_seq = self.getManualSequence()
            if self.hidden_seq is None:  # User cancelled
                return
        else:
            import random
            self.hidden_seq = [random.randint(1, self.k) for _ in range(self.k)]
        
        # Setup player
        is_auto_mode = self.auto_radio.isChecked()
        if is_auto_mode:
            self.auto_player = AutoPlayer()
        
        # Create new board
        self.board = MastermindBoard(self.k, self.n, is_auto_mode)
        if is_auto_mode:
            self.board.auto_play_button.clicked.connect(self.makeAutoMove)
        else:
            self.board.submit_button.clicked.connect(self.checkGuess)
        
        # Update layout
        old_board = self.board_widget
        self.board_widget = self.board
        self.centralWidget().layout().replaceWidget(old_board, self.board)
        old_board.deleteLater()
        
    def makeAutoMove(self):
        if self.game_over:
            return
            
        guess = self.auto_player.get_query(self.k)
        self.board.setGuess(guess)
        self.checkGuess()
        
    def checkGuess(self):
        if self.game_over:
            return
            
        guess = self.board.getCurrentGuess()
        if not guess:
            QMessageBox.warning(self, "Invalid Move", "Please fill all positions!")
            return
            
        exact, color = self.judge.check(self.k, self.hidden_seq, guess)
        self.board.updateFeedback(exact, color)
        
        if exact == self.k:
            QMessageBox.information(self, "Congratulations!", "You won!")
            self.game_over = True
        elif self.board.current_row == self.n - 1:
            QMessageBox.information(self, "Game Over", f"The sequence was {self.hidden_seq}")
            self.game_over = True
        else:
            self.board.current_row += 1
            self.board.current_col = 0

def main():
    app = QApplication(sys.argv)
    window = MastermindGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()