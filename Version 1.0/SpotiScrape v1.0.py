import tkinter as tk
from tkinter import ttk
import tkinter.messagebox  # Added for messagebox
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image, ImageTk
import io

# Spotify API credentials
client_id = '84d6cd4d6351419d8dc750a2768930ff'
client_secret = '94ca367fbd01433b8b01923d661c3431'

# Initialize Spotify client
sp = Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Variable to store the artwork URL
artwork_url = ""

# Function to extract song information
def scrape_spotify():
    global artwork_url  # Declare artwork_url as a global variable
    spotify_url = url_entry.get()

    try:
        track_info = sp.track(spotify_url)
        artist = track_info['artists'][0]['name']
        album = track_info['album']['name']
        track = track_info['name']
        artwork_url = track_info['album']['images'][0]['url']

        # Update labels with extracted information
        artist_label.config(text=f'Artist: {artist}')
        album_label.config(text=f'Album: {album}')
        track_label.config(text=f'Track: {track}')

        # Display artwork
        load_and_display_artwork(artwork_url)
        result_label.config(text='')

        # Enable the download button
        download_button.config(state=tk.NORMAL)

    except IndexError:
        result_label.config(text='Error: Invalid Spotify URL. Please enter a valid URL.')
    except Exception as e:
        result_label.config(text=f'Error: {str(e)}')

# Function to load and display artwork
def load_and_display_artwork(url):
    response = requests.get(url)
    img_data = response.content
    image = Image.open(io.BytesIO(img_data))
    image = ImageTk.PhotoImage(image)

    artwork_label.config(image=image)
    artwork_label.image = image

# Function to download and save the displayed artwork
def download_artwork():
    try:
        response = requests.get(artwork_url)
        img_data = response.content
        with open("artwork.png", "wb") as f:
            f.write(img_data)
        
        # Display a confirmation dialog
        tkinter.messagebox.showinfo("Download Confirmation", "Artwork saved as artwork.png")
        
    except Exception as e:
        result_label.config(text=f'Error downloading artwork: {str(e)}')

# Create the main window
root = tk.Tk()
root.title("Spotify Scraper")

# Create a canvas with a vertical scrollbar
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Create and place widgets inside the canvas
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

instruction_label = ttk.Label(frame, text="Enter a Spotify Song URL:")
instruction_label.pack(pady=10)

url_entry = ttk.Entry(frame, width=40)
url_entry.pack()

scrape_button = ttk.Button(frame, text="Scrape", command=scrape_spotify)
scrape_button.pack(pady=10)

result_label = ttk.Label(frame, text="", foreground="red")
result_label.pack()

# Organize the information labels and artwork
info_frame = ttk.Frame(frame)
info_frame.pack(pady=10)

artist_label = ttk.Label(info_frame, text="")
artist_label.pack()

album_label = ttk.Label(info_frame, text="")
album_label.pack()

track_label = ttk.Label(info_frame, text="")
track_label.pack()

artwork_label = ttk.Label(frame)
artwork_label.pack()

# Download Artwork Button (initially disabled)
download_button = ttk.Button(frame, text="Download Artwork", command=download_artwork, state=tk.DISABLED)
download_button.pack(pady=10)

# Bind the canvas to the frame for scrolling
frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()
