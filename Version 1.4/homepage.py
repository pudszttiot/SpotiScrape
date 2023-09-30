import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from main import SpotifyScraperApp

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SpotiScrape")
        self.setFixedSize(800, 600)
        self.setGeometry(300, 100, 800, 600)
        self.setWindowIcon(QIcon(r"..\Images\SpotiScrapeWindow1.ico"))

        # Create a QLabel to display the background image
        self.background_label = QLabel(self)
        pixmap = QPixmap(r"..\Images\SpotWallpaper6.jpg")  # Provide the path to your background image

        # Set the desired width and height for the background image
        desired_width = 1920
        desired_height = 1200
        pixmap = pixmap.scaled(desired_width, desired_height)

        # Calculate the position to center the background image
        label_x = int((self.width() - pixmap.width()) / 2)
        label_y = int((self.height() - pixmap.height()) / 2) - 90

        self.background_label.setGeometry(label_x, label_y, pixmap.width(), pixmap.height())
        self.background_label.setPixmap(pixmap)

        # Ensure the label is behind all other widgets
        self.background_label.lower()

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 800, 500)  # Cover the whole window
        pixmap = QPixmap(r"..\Images\SpotiScrapeLogo4.png")  # Provide the path to your image file

        # Define the desired width and height (adjust these values as needed)
        label_width = 800  # New width
        label_height = 500  # New height
        self.image_label.setPixmap(pixmap.scaled(label_width, label_height, aspectRatioMode=1))

        # Center the label in the window
        label_x = int((800 - label_width) / 2)
        label_y = int((600 - label_height) / 2) - 90
        self.image_label.move(label_x, label_y)

        # Create a button to open the main application page
        self.open_button = QPushButton("Open SpotiScrape", self)
        self.open_button.setGeometry(245, 450, 300, 70)
        self.open_button.clicked.connect(self.open_main_app)     

        # Apply custom style to the button
        self.open_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2b2b2b;
                color: #00db4d;
                border: 2px solid 006806;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #00db4d;
                color: #2b2b2b;
                border: 2px solid #0d0d0d;
                border-radius: 5px;
                font-size: 20px;
            }
            """
        )

    def open_main_app(self):
        self.main_app = SpotifyScraperApp()
        self.main_app.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    homepage = HomePage()
    homepage.show()
    sys.exit(app.exec_())
