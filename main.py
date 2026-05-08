from parser import get_all_followers, get_following
import tkinter as tk
from tkinter import filedialog
import ctypes

def main():
    
    
    root = tk.Tk()
    root.withdraw()
    # Select folder
    data_dir = filedialog.askdirectory(title="Select your Instagram Data Folder")
    
    if not data_dir:
        print("No folder selected. Exiting...")
        return

    # Use the functions from parser.py
    followers = get_all_followers(data_dir)
    following = get_following(data_dir)
    
    # Logic: Set Difference
    not_following_back = following - followers
    print(f"You follow {len(following)}")
    print(f"{len(followers)} people follow you")
    print(f"Found {len(not_following_back)} people who don't follow you back.")

    for user in sorted(not_following_back):
        print(user)
    

if __name__ == "__main__":
    main()