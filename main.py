import os
import time
import socket
import zipfile
import requests
from pystyle import Colors, Colorate

banner = """\n
              █████▒▄▄▄       ██▀███  ▓█████   ██████ ▄▄▄█████▓ ▒█████   ▒█████   ██▓
            ▓██   ▒▒████▄    ▓██ ▒ ██▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
            ▒████ ░▒██  ▀█▄  ▓██ ░▄█ ▒▒███   ░ ▓██▄   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
            ░▓█▒  ░░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
            ░▒█░    ▓█   ▓██▒░██▓ ▒██▒░▒████▒▒██████▒▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
             ▒ ░    ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
             ░       ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
             ░ ░     ░   ▒     ░░   ░    ░   ░  ░  ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
                         ░  ░   ░        ░  ░      ░               ░ ░      ░ ░      ░  ░
"""

def print_status(message):
    print(f"  {Colors.green} └──${Colors.white} {message}{Colors.reset}")

def load_game_data():
    return requests.get("https://fares.top/game_data.json").json()

def download_and_extract_zip(download_url, game_name):
    try:
        file_response = requests.get(download_url, stream=True, timeout=20, allow_redirects=True)
        zip_filename = f"{game_name}.zip"
        with open(zip_filename, "wb") as zip_file:
            for chunk in file_response.iter_content(chunk_size=8192):
                if chunk:
                    zip_file.write(chunk)
        print_status(f"Downloaded: {zip_filename}")
        extract_folder = os.path.splitext(zip_filename)[0]
        with zipfile.ZipFile(zip_filename, 'r') as archive:
            archive.extractall(extract_folder)
        print_status(f"Extracted to: {extract_folder}")
        os.remove(zip_filename)
        print_status(f"Cleaned up: {zip_filename}")
    except Exception as error:
        print_status(f"Download error: {error}")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Vertical(Colors.green_to_white, banner))
    print()
    computer_name = socket.gethostname()
    print(f"   {Colors.green}┌───({Colors.white}{computer_name}{Colors.green}){Colors.reset}")
    print_status("Loading game data...")
    game_data = load_game_data()
    user_input = input(f"   {Colors.green}└──${Colors.white} Enter AppID: {Colors.reset}").strip()

    if user_input:
        game_info = game_data.get(user_input)
        if game_info:
            zip_file = game_info["zip_file"]
            download_url = f"https://steamdatabase1.s3.eu-north-1.amazonaws.com/{zip_file}"
            download_and_extract_zip(download_url, game_info["game_name"])
        else:
            print_status("No game found with the provided AppID")
    else:
        print_status("No AppID provided")
