import os
import random
import time
import requests
import ctypes
from screeninfo import get_monitors

UNSPLASH_API_KEY = "REPLACE WITH YOUR UNPLASH API KEY"

def get_screen_resolution():
    # Get the screen resolution of the primary monitor
    monitors = get_monitors()
    primary_monitor = monitors[0]
    return primary_monitor.width, primary_monitor.height

def get_random_wallpaper(query, width, height):
    url = f"https://api.unsplash.com/photos/random?query={query}&w={width}&h={height}"
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["urls"]["full"]
    else:
        print(f"Failed to fetch wallpaper. Status code: {response.status_code}")
        return None

def set_wallpaper(image_url, filename):
    try:
        # Get the current working directory
        current_directory = os.getcwd()
        # Create the full path to save the image in the same folder as the script
        save_path = os.path.join(current_directory, filename)

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            # Set the downloaded image as the wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, save_path, 3)
            print(f"Wallpaper set to {save_path}")
        else:
            print("Failed to download image.")
    except Exception as e:
        print(f"Failed to set wallpaper: {str(e)}")

if __name__ == "__main__":
    while True:
        query = input("Enter the type of wallpapers you want (e.g., 'sci-fi', 'cars'): ")
        width, height = get_screen_resolution()  # Automatically detect screen resolution
        wallpaper_url = get_random_wallpaper(query, width, height)
        
        if wallpaper_url:
            # Define a filename for the downloaded image
            image_filename = 'downloaded_wallpaper.jpg'

            # Call the function to set the wallpaper
            set_wallpaper(wallpaper_url, image_filename)
        else:
            print("Unable to fetch a wallpaper that matches your criteria.")

        # Wait for 10 minutes before changing the wallpaper again
        time.sleep(600)  # 10 minutes = 600 seconds
