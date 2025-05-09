################################################################
# Author: Julia Kaczmarek 
# Date : 09-05-2025
# This is a simple writing tracker created for my girlfriend. It takes in
# int input for the number of words needed to be written, the number of words currently written,
# and the number of days until the deadline. It calculates the number of words needed to be written per day
# the main window contains a jar which fills up with sweets as the user writes more words.
# The data is saved in a json file, which is kept and opened when the program is ran.
# The program is created using PySide6 and is a simple GUI application.

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QInputDialog
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, Signal, QObject
import sys
import json
from collections import UserDict
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QDialogButtonBox
import datetime
from PySide6.QtWidgets import QProgressBar

class writing_data_signals(QObject):
    updated = Signal()

class writing_data(UserDict):
    def __init__(self, *args, **kwargs):
        self.signals = writing_data_signals()
        super().__init__(*args, **kwargs)
    def __setitem__(self, key, value):
        prev_value = self.get(key)
        super().__setitem__(key, value)
        if value != prev_value:
            self.signals.updated.emit()

writing_data = writing_data(
    {
        "word_count": 0,
        "word_goal": 0,
        "deadline_date": None
    }
)

class WritingTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alex's Writing Tracker")
        self.setGeometry(100, 100, 300, 350)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.custom_title_bar = QWidget(self)
        self.custom_title_bar.setFixedHeight(30)
        self.custom_title_bar.setStyleSheet("background-color: #FF69B4;")
        title_layout = QHBoxLayout(self.custom_title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)
        title_layout.setSpacing(5)
        title_label = QLabel("Alex's Writing Tracker", self.custom_title_bar)
        title_label.setStyleSheet("color: white; font-family: 'Comic Sans MS'; font-size: 16px;")
        title_layout.addWidget(title_label)
        # title_layout.addStretch()
        close_btn = QPushButton("X", self.custom_title_bar)
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("background: transparent; color: white; border: none;")
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        def mousePressEvent(event):
            if event.button() == Qt.LeftButton:
                self._offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

        def mouseMoveEvent(event):
            if event.buttons() == Qt.LeftButton and hasattr(self, "_offset"):
                self.move(event.globalPosition().toPoint() - self._offset)

        self.custom_title_bar.mousePressEvent = mousePressEvent
        self.custom_title_bar.mouseMoveEvent = mouseMoveEvent

        self.main_layout.addWidget(self.custom_title_bar)
        
        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        # self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.main_layout.addWidget(self.central_widget)

        # Set main_widget as the central widget of QMainWindow
        self.setCentralWidget(self.main_widget)

        self.setStyleSheet("background-color: #FFF0F5;")
        header = QLabel("Welcome, Beautiful Dreamer!")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(
            "font-family: 'Comic Sans MS'; font-size: 24px; color: #FF69B4;"
            "background-color: #FFF0F5; border: 2px dashed #FF69B4; border-radius: 10px; padding: 10px;"
        )
        self.fun_header = header
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.addWidget(self.fun_header)
        self.layout.setAlignment(Qt.AlignTop)
        self.goal_layout = QHBoxLayout()
        self.layout.addLayout(self.goal_layout)
        self.count_layout = QHBoxLayout()
        self.layout.addLayout(self.count_layout)
        self.days_layout = QHBoxLayout()
        self.layout.addLayout(self.days_layout)
        
        self.count_layout.setAlignment(Qt.AlignCenter)
        self.word_count_label = QLabel("Word Count:")
        self.word_count_label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px; font-weight: bold; color: #FF69B4;")
        self.count_layout.addWidget(self.word_count_label)
        self.word_count_input = QLineEdit()
        self.word_count_input.setValidator(QIntValidator())
        self.word_count_input.textChanged.connect(lambda: writing_data.__setitem__("word_count", int(self.word_count_input.text()) if self.word_count_input.text() else 0))
        self.word_count_input.setPlaceholderText("Enter word count")
        self.word_count_input.setAlignment(Qt.AlignCenter)
        self.word_count_input.setFixedWidth(150)
        self.word_count_input.setFixedHeight(30)
        self.word_count_input.setStyleSheet(
            "font-family: 'Comic Sans MS'; font-size: 14px; background-color: #FFF0F5; "
            "border: 1px solid #FF69B4; border-radius: 5px; padding: 5px; color: #FF69B4;"
        )
        self.count_layout.addWidget(self.word_count_input)
        
        self.goal_layout.setAlignment(Qt.AlignCenter)
        self.word_goal_label = QLabel("Word Goal:")
        self.word_goal_label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px; font-weight: bold; color: #FF69B4;")
        self.goal_layout.addWidget(self.word_goal_label)
        self.word_goal_input = QLineEdit()
        self.word_goal_input.setValidator(QIntValidator())
        self.word_goal_input.textChanged.connect(lambda: writing_data.__setitem__("word_goal", int(self.word_goal_input.text()) if self.word_goal_input.text() else 0))
        self.word_goal_input.setPlaceholderText("Enter word goal")
        self.word_goal_input.setAlignment(Qt.AlignCenter)
        self.word_goal_input.setFixedWidth(150)
        self.word_goal_input.setFixedHeight(30)
        self.word_goal_input.setStyleSheet(
            "font-family: 'Comic Sans MS'; font-size: 14px; background-color: #FFF0F5; "
            "border: 1px solid #FF69B4; border-radius: 5px; padding: 5px; color: #FF69B4;"
        )
        self.goal_layout.addWidget(self.word_goal_input)
        
        self.days_layout.setAlignment(Qt.AlignCenter)
        self.days_left_label = QLabel(f"Days Left: {self.days_left if hasattr(self, 'days_left') else 0}")
        self.days_left_label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px; color: #FF69B4;")
        self.days_layout.addWidget(self.days_left_label)
        self.input_deadline = QPushButton("Set Deadline")
        self.input_deadline.setStyleSheet(
            "font-family: 'Comic Sans MS'; font-size: 14px; background-color: #FFF0F5; "
            "border: 1px solid #FF69B4; border-radius: 5px; padding: 5px; color: #FF69B4;"
        )
        self.input_deadline.clicked.connect(self.update_deadline)
        self.days_layout.addWidget(self.input_deadline)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(35)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            "QProgressBar {"
            "    border: 1px solid #FF69B4;"
            "    border-radius: 10px;"
            "    background-color: #FFF0F5;"
            "}"
            "QProgressBar::chunk {"
            "    border-radius: 10px;"
            "    background-color: qlineargradient("
            "        spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "        stop:0 #FF69B4, stop:0.5 #FFB6C1, stop:1 #FF69B4"
            "    );"
            "}"
        )
        self.layout.addWidget(self.progress_bar)

        self.percent_label = QLabel(f"Percent of Goal Achieved: {self.percent if hasattr(self, 'percent') else 0}%")
        self.percent_label.setAlignment(Qt.AlignCenter)
        self.percent_label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px; color: #FF69B4;")
        self.layout.addWidget(self.percent_label)
        
        self.words_per_day_label = QLabel(f"Need to write {self.words_per_day if hasattr(self, 'words_per_day') else 0} words per day to make it")
        self.words_per_day_label.setAlignment(Qt.AlignCenter)
        self.words_per_day_label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 14px; color: #FF69B4;")
        self.layout.addWidget(self.words_per_day_label)
        self.central_layout.addLayout(self.layout)
        self.load_data()

    def load_data(self):
        try:
            with open("writing_data.json", "r") as f:
                data = json.load(f)
                writing_data.update(data)
                self.word_count_input.setText(str(writing_data["word_count"]))
                self.word_goal_input.setText(str(writing_data["word_goal"]))
                self.days_left = writing_data["deadline_date"]
                self.update_days_left()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass
        except KeyError:
            pass
        except Exception as e:
            print(f"Error loading data: {e}")
        writing_data.signals.updated.connect(self.update_ui)

    def update_deadline(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Deadline Date")
        layout = QVBoxLayout(dialog)
        calendar = QCalendarWidget(dialog)
        calendar.setGridVisible(True)
        layout.addWidget(calendar)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=dialog)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        if dialog.exec() == QDialog.Accepted:
            selected = calendar.selectedDate()
            deadline = datetime.date(selected.year(), selected.month(), selected.day())
            today = datetime.date.today()
            days_left = (deadline - today).days
            self.days_left = days_left
            writing_data["deadline_date"] = deadline.isoformat()
            self.days_left_label.setText(f"Days Left: {days_left}")

    def update_ui(self):
        self.word_count_input.setText(str(writing_data["word_count"]))
        self.word_goal_input.setText(str(writing_data["word_goal"]))
        # self.update_days_left()
        # self.update_percent()
        # self.update_words_per_day()
        # self.save_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WritingTracker()
    window.show()
    sys.exit(app.exec())