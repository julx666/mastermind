import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from judge import Judge
from player import AutoPlayer


class PegWidget(QWidget):
    """
    A custom QWidget representing a colored peg in a Mastermind game.

    Attributes:
        color (QColor): The color of the peg. Default is Qt.gray.
        size (int): The size of the peg. Default is 30.
    """

    def __init__(self, color=Qt.gray, size=30):
        super().__init__()
        self.color = color
        self.setFixedSize(QSize(size, size))

    def paintEvent(self, event):
        """
        Handles the paint event for the widget.

        This method is called whenever the widget needs to be repainted. It uses
        QPainter to draw an ellipse with the specified color and dimensions.

        Args:
            event (QPaintEvent): The paint event that triggered this method.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)

    def setColor(self, color):
        """
        Sets the color attribute and triggers an update.

        Args:
            color (str): The color to be set.
        """
        self.color = color
        self.update()


class MastermindBoard(QWidget):
    """
    A QWidget subclass representing the Mastermind game board.

    Attributes:
        COLORS (list): List of QColor objects representing the available colors.
        k (int): Number of colors to choose from.
        n (int): Number of rows in the game board.
        seq_l (int): Length of the sequence to guess.
        current_row (int): Index of the current row being played.
        current_col (int): Index of the current column being played.
        is_auto_mode (bool): Flag indicating if the game is in auto mode.
        pegs (list): 2D list of PegWidget objects representing the main pegs.
        feedback_pegs (list): 2D list of PegWidget objects representing the feedback pegs.
        submit_button (QPushButton): Button to submit the current guess (only in manual mode).
        auto_play_button (QPushButton): Button to make an automatic move (only in auto mode).

    """

    COLORS = [
        QColor(Qt.red),
        QColor(Qt.blue),
        QColor(Qt.green),
        QColor(Qt.yellow),
        QColor(Qt.cyan),
        QColor(Qt.magenta),
    ]

    def __init__(self, seq_l, k, n, is_auto_mode=False):
        """
        Initializes the game interface.

        Args:
            seq_l (int): The length of the sequence to guess.
            k (int): The number of possible values for each position in the sequence.
            n (int): The number of attempts allowed to guess the sequence.
            is_auto_mode (bool, optional): If True, the game will run in automatic mode. Defaults to False.
        """
        super().__init__()
        self.k = k
        self.n = n
        self.seq_l = seq_l
        self.current_row = 0
        self.current_col = 0
        self.is_auto_mode = is_auto_mode
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface for the Mastermind game.

        This method sets up the game board with pegs and feedback pegs, and adds
        color selection buttons and a submit button in manual mode, or an auto play
        button in automatic mode.

        Attributes:
            layout (QGridLayout): The main layout for the game board.
            pegs (list): A list of lists containing PegWidget objects for the main pegs.
            feedback_pegs (list): A list of lists containing PegWidget objects for the feedback pegs.
            color_widget (QWidget): The widget containing color selection buttons (manual mode only).
            color_layout (QHBoxLayout): The layout for the color selection buttons (manual mode only).
            submit_button (QPushButton): The button to submit the player's guess (manual mode only).
            auto_play_button (QPushButton): The button to make an automatic move (automatic mode only).

        Note:
            This method assumes that `self.n`, `self.seq_l`, `self.COLORS`, `self.k`, and `self.is_auto_mode`
            are already defined in the class.
        """
        layout = QGridLayout()
        self.pegs = []
        self.feedback_pegs = []

        # Create game board
        for row in range(self.n):
            row_pegs = []
            row_feedback = []

            # Main pegs
            for col in range(self.seq_l):
                peg = PegWidget(QColor(Qt.gray))
                layout.addWidget(peg, row, col)
                row_pegs.append(peg)

            # Feedback pegs
            feedback_widget = QWidget()
            feedback_layout = QGridLayout()
            for i in range(self.seq_l):
                feedback_peg = PegWidget(QColor(Qt.gray), size=15)
                feedback_layout.addWidget(feedback_peg, 1, i)
                row_feedback.append(feedback_peg)

            feedback_widget.setLayout(feedback_layout)
            layout.addWidget(feedback_widget, row, self.seq_l)

            self.pegs.append(row_pegs)
            self.feedback_pegs.append(row_feedback)

        # Only show color selection and submit button in manual mode
        if not self.is_auto_mode:
            # Color selection
            color_widget = QWidget()
            color_layout = QHBoxLayout()
            for i, color in enumerate(self.COLORS[: self.k]):
                color_button = QPushButton()
                color_button.setFixedSize(QSize(30, 30))
                color_button.setStyleSheet(f"background-color: {color.name()}")
                color_button.clicked.connect(
                    lambda checked, c=color: self.selectColor(c)
                )
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
        """
        Selects a color for the current peg in the current row and column, then moves to the next column.

        Args:
            color (str): The color to set for the current peg.

        Notes:
            - The method only sets the color if the current row is less than the total number of rows (n)
              and the current column is less than the sequence length (seq_l).
            - After setting the color, the current column is incremented. If it reaches the sequence length,
              it wraps around to the first column.
        """
        if self.current_row < self.n and self.current_col < self.seq_l:
            self.pegs[self.current_row][self.current_col].setColor(color)
            self.current_col = (self.current_col + 1) % self.seq_l

    def getCurrentGuess(self):
        """
        Retrieves the current guess from the pegs in the current row.

        Iterates over the pegs in the current row and collects their colors.
        If any peg has the color gray, it returns None indicating an incomplete guess.
        Otherwise, it returns a list of integers representing the indices of the colors.

        Returns:
            list[int] or None: A list of integers representing the color indices of the current guess,
                               or None if the guess is incomplete.
        """
        guess = []
        for peg in self.pegs[self.current_row]:
            color = peg.color
            if color == QColor(Qt.gray):
                return None
            guess.append(self.COLORS.index(color) + 1)
        return guess

    def setGuess(self, guess):
        """
        Sets the colors of the pegs in the current row based on the provided guess.

        Args:
            guess (list of int): A list of integers representing the guessed colors.
                                 Each integer corresponds to a color index.

        """
        for i, num in enumerate(guess):
            self.pegs[self.current_row][i].setColor(self.COLORS[num - 1])
        self.current_col = self.seq_l

    def updateFeedback(self, exact, color):
        """
        Updates the feedback pegs for the current row based on the number of exact matches
        and color matches.

        Args:
            exact (int): The number of pegs that are the correct color and in the correct position.
            color (int): The number of pegs that are the correct color but in the wrong position.
        """
        feedback_row = self.feedback_pegs[self.current_row]
        idx = 0

        for _ in range(exact):
            feedback_row[idx].setColor(QColor(Qt.black))
            idx += 1

        for _ in range(color):
            feedback_row[idx].setColor(QColor(Qt.white))
            idx += 1


class MastermindGUI(QMainWindow):
    """
    MastermindGUI is a class that represents the graphical user interface for the Mastermind game.
    It inherits from QMainWindow and provides methods to initialize the game, set up the UI, and handle game logic.
    """

    def __init__(self):
        """
        Initializes the main window of the application.

        This constructor method calls the parent class constructor and initializes
        the game and user interface components by calling the initGame and initUI methods.
        """
        super().__init__()
        self.initGame()
        self.initUI()

    def initGame(self):
        """
        Initializes the game with default settings.

        This method sets up the initial parameters for the game, including:
        - `k`: The number of possible colors.
        - `seq_l`: The length of the sequence to guess.
        - `n`: The number of attempts allowed.
        - `judge`: An instance of the Judge class to evaluate guesses.
        - `hidden_seq`: The hidden sequence to be guessed, initially set to None.
        - `game_over`: A flag indicating whether the game is over, initially set to False.
        - `auto_player`: An optional automated player, initially set to None.
        """
        self.k = 4
        self.seq_l = 6
        self.n = 10
        self.judge = Judge()
        self.hidden_seq = None
        self.game_over = False
        self.auto_player = None

    def initUI(self):
        """
        Initializes the user interface for the Mastermind game.

        This method sets up the main window, including the title, geometry, and layout.
        It creates and configures various widgets such as spin boxes for selecting the number
        of colors (K) and sequence length (N), radio buttons for selecting the game mode
        (Auto Player or Manual Player), and options for selecting the hidden sequence in auto mode.
        It also includes a start button to begin the game and a placeholder for the game board.

        Widgets created:
            - QLabel: Labels for colors, sequence length, game mode, and hidden sequence.
            - QSpinBox: Spin boxes for selecting the number of colors (K) and sequence length (N).
            - QRadioButton: Radio buttons for selecting the game mode and hidden sequence options.
            - QPushButton: Button to start the game.
            - QWidget: Central widget and placeholders for layout and game board.
            - QVBoxLayout, QHBoxLayout: Layouts to organize the widgets.

        Connections:
            - self.auto_radio.toggled: Connects to updateSequenceOptions to update sequence options based on game mode.
            - self.start_button.clicked: Connects to startGame to start the game when the button is clicked.
        """
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

        # Seq_l selection
        n_layout = QVBoxLayout()
        n_label = QLabel("Sequence length (N):")
        self.n_spin = QSpinBox()
        self.n_spin.setRange(1, 10)
        self.n_spin.setValue(self.seq_l)
        n_layout.addWidget(n_label)
        n_layout.addWidget(self.n_spin)
        config_layout.addLayout(n_layout)

        # Game mode selection
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Game Mode:")
        self.auto_radio = QRadioButton("Auto Player")
        self.manual_radio = QRadioButton("Manual Player")
        self.manual_radio.setChecked(True)

        # Connect radio buttons to update sequence options
        self.auto_radio.toggled.connect(self.updateSequenceOptions)

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.auto_radio)
        mode_layout.addWidget(self.manual_radio)
        config_layout.addLayout(mode_layout)

        # Sequence selection (only visible in auto mode)
        self.seq_layout = QVBoxLayout()
        seq_label = QLabel("Hidden Sequence:")
        self.random_seq_radio = QRadioButton("Random")
        self.manual_seq_radio = QRadioButton("Manual")
        self.random_seq_radio.setChecked(True)
        self.seq_layout.addWidget(seq_label)
        self.seq_layout.addWidget(self.random_seq_radio)
        self.seq_layout.addWidget(self.manual_seq_radio)

        # Create a widget to hold the sequence options
        self.seq_widget = QWidget()
        self.seq_widget.setLayout(self.seq_layout)
        self.seq_widget.hide()  # Initially hidden
        config_layout.addWidget(self.seq_widget)

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

    def updateSequenceOptions(self, checked):
        """
        Updates the visibility of the sequence options widget based on the given checkbox state.

        Args:
            checked (bool): The state of the checkbox. If True, the sequence options widget will be visible.
        """
        self.seq_widget.setVisible(checked)

    def getManualSequence(self):
        """
        Prompts the user to enter a hidden sequence of numbers via a dialog box.

        The user is asked to input a sequence of numbers separated by commas. The input is validated to ensure
        it contains the correct number of elements and that each element is within the specified range.

        Returns:
            list: A list of integers representing the hidden sequence if the input is valid.
            None: If the user cancels the input dialog.

        Raises:
            ValueError: If the input contains non-integer values or if the numbers are out of the specified range.
        """
        sequence = []
        valid_input = False

        while not valid_input:
            text, ok = QInputDialog.getText(
                self,
                "Enter Hidden Sequence",
                f"Enter {self.seq_l} numbers (1-{self.k}) separated by commas:",
            )

            if not ok:
                return None

            try:
                sequence = [int(x.strip()) for x in text.split(",")]
                if len(sequence) != self.seq_l or not all(
                    1 <= x <= self.k for x in sequence
                ):
                    QMessageBox.warning(
                        self,
                        "Invalid Input",
                        f"Please enter exactly {self.seq_l} numbers between 1 and {self.k}",
                    )
                    continue
                valid_input = True
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers")

        return sequence

    def startGame(self):
        """
        Initializes and starts a new game of Mastermind.

        This method sets up the game parameters based on user input, generates the hidden sequence,
        and configures the game board and player mode.

        Steps:
        1. Retrieves the values for the number of colors (k) and the sequence length (seq_l) from the UI.
        2. Determines the game mode (manual or auto) and generates the hidden sequence accordingly.
        3. Sets up the player mode (manual or auto).
        4. Creates a new game board and connects the appropriate signals for user interaction.
        5. Updates the UI to display the new game board.

        If the user cancels the manual sequence input, the game initialization is aborted.

        Returns:
            None
        """
        self.k = self.k_spin.value()
        self.seq_l = self.n_spin.value()
        self.game_over = False

        # Generate hidden sequence based on game mode
        if self.manual_radio.isChecked():
            # Manual player mode - always random sequence
            import random

            self.hidden_seq = [random.randint(1, self.k) for _ in range(self.seq_l)]
        else:
            # Auto player mode - check sequence option
            if self.manual_seq_radio.isChecked():
                self.hidden_seq = self.getManualSequence()
                if self.hidden_seq is None:  # User cancelled
                    return
            else:
                import random

                self.hidden_seq = [random.randint(1, self.k) for _ in range(self.seq_l)]

        # Setup player
        is_auto_mode = self.auto_radio.isChecked()
        if is_auto_mode:
            self.auto_player = AutoPlayer()

        # Create new board
        self.board = MastermindBoard(self.seq_l, self.k, self.n, is_auto_mode)
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
        """
        Makes an automatic move in the game.

        This method is called to make a move on behalf of the automated player.
        It first checks if the game is over. If the game is not over, it gets a
        guess from the automated player, sets the guess on the board, and then
        checks the guess.

        Returns:
            None
        """
        if self.game_over:
            return

        guess = self.auto_player.get_query(self.seq_l, self.k)
        self.board.setGuess(guess)
        self.checkGuess()

    def checkGuess(self):
        """
        Checks the current guess made by the player and provides feedback.

        If the game is over, the method returns immediately. Otherwise, it retrieves
        the current guess from the board. If the guess is incomplete, a warning message
        is shown. The guess is then checked against the hidden sequence, and feedback
        is provided on the board.

        If the guess is correct, a congratulatory message is shown and the game ends.
        If the guess is incorrect and the player has no more attempts left, a game over
        message is shown with the correct sequence. Otherwise, the method advances to
        the next row for the player to make another guess.

        Returns:
            None
        """
        if self.game_over:
            return

        guess = self.board.getCurrentGuess()
        if not guess:
            QMessageBox.warning(self, "Invalid Move", "Please fill all positions!")
            return

        exact, color = self.judge.check(self.k, self.hidden_seq, guess)
        self.board.updateFeedback(exact, color)

        if exact == self.seq_l:
            QMessageBox.information(self, "Congratulations!", "You won!")
            self.game_over = True
        elif self.board.current_row == self.n - 1:
            QMessageBox.information(
                self, "Game Over", f"The sequence was {self.hidden_seq}"
            )
            self.game_over = True
        else:
            self.board.current_row += 1
            self.board.current_col = 0


def main():
    """
    Main function to start the Mastermind GUI application.

    This function initializes the QApplication, creates an instance of the
    MastermindGUI window, displays it, and starts the application's event loop.

    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = MastermindGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
