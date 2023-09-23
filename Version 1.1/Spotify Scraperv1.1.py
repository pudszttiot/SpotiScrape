import sys
import requests
from PIL import Image
import io
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QImage, QFont, QIcon, QPixmap, QClipboard
from PyQt5.QtWidgets import QApplication, QScrollArea, QSizePolicy, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from urllib.parse import urlparse

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
client_id = '84d6cd4d6351419d8dc750a2768930ff'
client_secret = '94ca367fbd01433b8b01923d661c3431'

# Initialize Spotify client
sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

class SpotifyScraperApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Spotify Scraper")
        self.setWindowIcon(QIcon('ENTER_ICON_IMAGE.png'))  # Replace with the path to your Spotify logo image

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)

        self.central_widget = QWidget(self)
        scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(scroll_area)

        layout = QVBoxLayout()

        # Add custom fonts
        font = QFont("Helvetica", 14)

        self.instruction_label = QLabel("Enter a Spotify Song URL:")
        self.instruction_label.setFont(font)
        layout.addWidget(self.instruction_label)

        self.url_entry = QLineEdit()
        self.url_entry.setFont(font)
        self.url_entry.setPlaceholderText("https://open.spotify.com/track/")  # Placeholder text
        layout.addWidget(self.url_entry)

        # Create a horizontal layout for the Scrape button
        scrape_button_layout = QHBoxLayout()
        scrape_button_layout.addStretch(1)
        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.setFont(font)
        self.scrape_button.setStyleSheet("background-color: #1DB954; color: white;")
        self.scrape_button.setToolTip("Click to scrape Spotify information")  # Tooltip
        self.scrape_button.clicked.connect(self.scrape_spotify)
        self.scrape_button.setFixedSize(150, 40)
        scrape_button_layout.addWidget(self.scrape_button)
        scrape_button_layout.addStretch(1)
        layout.addLayout(scrape_button_layout)

        self.result_label = QLabel()
        self.result_label.setFont(font)
        layout.addWidget(self.result_label)

        self.artist_label = QLabel()
        self.artist_label.setFont(font)
        layout.addWidget(self.artist_label)

        self.album_label = QLabel()
        self.album_label.setFont(font)
        layout.addWidget(self.album_label)

        self.track_label = QLabel()
        self.track_label.setFont(font)
        layout.addWidget(self.track_label)

        self.artwork_label = QLabel()
        layout.addWidget(self.artwork_label)

        # Create a horizontal layout for the Download Artwork button
        download_button_layout = QHBoxLayout()
        download_button_layout.addStretch(1)
        self.download_button = QPushButton("Download Artwork")
        self.download_button.setFont(font)
        self.download_button.setStyleSheet("background-color: #1DB954; color: white;")
        self.download_button.setToolTip("Click to download artwork image")  # Tooltip
        self.download_button.clicked.connect(self.download_artwork)
        self.download_button.setFixedSize(180, 40)
        self.download_button.setEnabled(False)
        download_button_layout.addWidget(self.download_button)
        download_button_layout.addStretch(1)
        layout.addLayout(download_button_layout)

        # Enhancement 1: Add a Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(font)
        self.clear_button.setToolTip("Click to clear results")
        self.clear_button.clicked.connect(self.clear_input)
        self.clear_button.setFixedSize(100, 40)
        layout.addWidget(self.clear_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.central_widget.setLayout(layout)

        # Add a background color or image that matches Spotify
        self.setStyleSheet("background-color: #191414; color: white;")

        # Enhancement 3: Set default focus to URL entry field
        self.url_entry.setFocus()

        # Change tooltip colors
        self.setStyleSheet("""
            QToolTip {
                background-color: #1DB954;
                color: white;
                border: 1px solid #FF5733;
            }
        """)

    def scrape_spotify(self):
        spotify_url = self.url_entry.text()

        if not self.is_valid_spotify_url(spotify_url):
            self.show_error_message('Error: Invalid Spotify URL. Please enter a valid URL.')
            return

        try:
            track_info = sp.track(spotify_url)
            artist = track_info['artists'][0]['name']
            album = track_info['album']['name']
            track = track_info['name']
            artwork_url = track_info['album']['images'][0]['url']

            self.artist_label.setText(f'Artist: {artist}')
            self.album_label.setText(f'Album: {album}')
            self.track_label.setText(f'Track: {track}')

            self.load_and_display_artwork(artwork_url)
            self.result_label.setText('')

            self.artwork_url = artwork_url
            self.download_button.setEnabled(True)

        except IndexError:
            self.show_error_message('Error: Invalid Spotify URL. Please enter a valid URL.')
        except Exception as e:
            error_message = f'Error: {str(e)}'
            print(error_message)  # Print the error to the console for debugging purposes.
            self.show_error_message(error_message)

    def load_and_display_artwork(self, url):
        response = requests.get(url)
        img_data = response.content
        image = Image.open(io.BytesIO(img_data))
        image = image.convert("RGBA")
        image_data = image.tobytes("raw", "RGBA")
        q_image = QImage(image_data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        self.artwork_label.setPixmap(pixmap)

    def download_artwork(self):
        try:
            response = requests.get(self.artwork_url)
            img_data = response.content
            with open("artwork.png", "wb") as f:
                f.write(img_data)
            self.result_label.setText('Artwork saved as artwork.png')

            # Show a dialog box indicating successful image save
            QMessageBox.information(self, "Success", "Artwork saved successfully.")

        except Exception as e:
            error_message = f'Error downloading artwork: {str(e)}'
            self.show_error_message(error_message)

    def show_error_message(self, message, is_copy_enabled=True):
        error_message_box = QMessageBox(self)
        error_message_box.setIcon(QMessageBox.Critical)
        error_message_box.setWindowTitle("Error")
        error_message_box.setText(message)
        if is_copy_enabled:
            error_message_box.addButton(QMessageBox.Copy)
        error_message_box.exec()

        # Copy error message to clipboard if the "Copy" button is clicked
        if is_copy_enabled and error_message_box.clickedButton() == error_message_box.button(QMessageBox.Copy):
            clipboard = QApplication.clipboard()
            clipboard.setMimeData(QMimeData().setText(message))

    # Enhancement 1: Clear Input Field
    def clear_input(self):
        self.url_entry.clear()
        self.result_label.clear()
        self.artist_label.clear()
        self.album_label.clear()
        self.track_label.clear()
        self.artwork_label.clear()
        self.download_button.setEnabled(False)

    def is_valid_spotify_url(self, url):
        # Check if the URL matches a Spotify track URL
        parsed_url = urlparse(url)
        return parsed_url.netloc == "open.spotify.com" and parsed_url.path.startswith("/track/")

    # Connect the URL entry field change event to the validation function
    def url_entry_changed(self):
        # Enable or disable buttons based on the validity of the URL input
        url = self.url_entry.text()
        is_valid_url = self.is_valid_spotify_url(url)
        self.scrape_button.setEnabled(is_valid_url)
        self.download_button.setEnabled(is_valid_url)

def main():
    app = QApplication(sys.argv)
    window = SpotifyScraperApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
