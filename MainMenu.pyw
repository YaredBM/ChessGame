import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
from tkinter import messagebox
import sys
from tkinter import simpledialog

# Base directory for dynamic paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "Menu")

# def start_game():
#     """Start the game."""
#     if not selected_mode.get() or not selected_style.get() or not selected_language.get():
#         tk.messagebox.showwarning("Missing Selection", "Please select mode, style, and language before starting!")
#         return
#     main_menu_root.destroy()
#     subprocess.Popen(["python", os.path.join(BASE_DIR, "Chess_copy.pyw"), selected_style.get()])

def start_game():
    """Start the game."""
    if not selected_mode.get() or not selected_style.get() or not selected_language.get():
        tk.messagebox.showwarning("Missing Selection", "Please select mode, style, and language before starting!")
        return

    # Show name input window based on selected mode
    get_player_names(selected_mode.get())

def get_player_names(mode):
    """Open a custom window to get player names based on the game mode."""
    def submit_names():
        # Get entered names
        p1_name = player1_entry.get().strip()
        p2_name = player2_entry.get().strip() if mode == "1 VS 1" else "AI"

        if not p1_name or (mode == "1 VS 1" and not p2_name):
            tk.messagebox.showwarning("Missing Names", "Please fill in all the fields!")
            return

        # Close the name input window
        name_window.destroy()

        # Start the game with names, style, and language
        main_menu_root.destroy()
        subprocess.Popen([
            "python",
            os.path.join(BASE_DIR, "Chess.pyw"),
            selected_style.get(),
            p1_name,
            p2_name,
            selected_language.get()
        ])
    # Create the name input window
    name_window = tk.Toplevel(main_menu_root)
    name_window.title("Enter Player Names")
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")
    name_window.iconbitmap(icon_path)

    # Define window dimensions
    window_width = 400
    window_height = 300

    # Center the window
    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    name_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    name_window.configure(bg="#4A646C")

    # Titles
    tk.Label(name_window, text="Enter Player Names", font=("Arial", 20, "bold"), bg="#4A646C", fg="white").pack(pady=10)

    # Player 1 Name Entry
    tk.Label(name_window, text="Player 1 Name:", font=("Arial", 14), bg="#4A646C", fg="white").pack(pady=5)
    player1_entry = tk.Entry(name_window, font=("Arial", 14))
    player1_entry.pack(pady=5)

    # Player 2 Name Entry (if applicable)
    if mode == "1 VS 1":
        tk.Label(name_window, text="Player 2 Name:", font=("Arial", 14), bg="#4A646C", fg="white").pack(pady=5)
        player2_entry = tk.Entry(name_window, font=("Arial", 14))
        player2_entry.pack(pady=5)
    else:
        player2_entry = None

    # Confirm Button
    tk.Button(name_window, text="Start Game", font=("Arial", 14, "bold"), bg="#E87A59", fg="white",
              command=submit_names).pack(pady=20)


def main_menu():
    """Create and display the main menu."""
    global main_menu_root, selected_mode, selected_style, selected_language

    # Main window
    main_menu_root = tk.Tk()
    main_menu_root.title("Welcome to Chess")
    main_menu_root.configure(bg="#4A646C")
    main_menu_root.state("zoomed")
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")
    main_menu_root.iconbitmap(icon_path)

    # Initialize variables
    selected_mode = tk.StringVar()
    selected_style = tk.StringVar()
    selected_language = tk.StringVar()

    # Main frame
    main_container = tk.Frame(main_menu_root, bg="#4A646C")
    main_container.pack(expand=True)

    # Title
    tk.Label(main_container, text="Welcome to Chess", font=("Arial", 45, "bold"), bg="#4A646C", fg="white").pack(pady=20)

    # Game Mode
    tk.Label(main_container, text="Choose your game mode:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    mode_frame = tk.Frame(main_container, bg="#4A646C")
    mode_frame.pack()

    for mode, file in [("1 VS 1", "1vs1.png"), ("1 VS AI", "1vsAI.png")]:
        img_path = os.path.join(ASSETS_DIR, file)
        img = Image.open(img_path).resize((230, 130), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        btn = tk.Radiobutton(mode_frame, image=img, variable=selected_mode, value=mode, indicatoron=False,
                             bg="#4A646C", selectcolor="#4A646C", borderwidth=0)
        btn.image = img
        btn.pack(side="left", padx=10)

    # Styles
    tk.Label(main_container, text="Choose your style:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    style_frame = tk.Frame(main_container, bg="#4A646C")
    style_frame.pack()

    for style, file in [("Baby", "baby.png"), ("Wood", "wood.png"), ("Spooky", "spooky.png"), ("Nightly", "nightly.png"), ("Love", "love.png")]:
        img_path = os.path.join(ASSETS_DIR, file)
        img = Image.open(img_path).resize((80, 80), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        container = tk.Frame(style_frame, bg="#4A646C")
        container.pack(side="left", padx=20)
        tk.Radiobutton(container, image=img, variable=selected_style, value=style, indicatoron=False,
                       bg="#4A646C", borderwidth=0).pack()
        container.image = img
        tk.Label(container, text=style, font=("Arial", 14), bg="#4A646C", fg="white").pack()

    # Language Selection
    tk.Label(main_container, text="Choose your language:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    language_frame = tk.Frame(main_container, bg="#4A646C")
    language_frame.pack()

    for lang, file in [("Spanish", "spanish.png"), ("English", "english.png"), ("Turkish", "turkish.png")]:
        img_path = os.path.join(ASSETS_DIR, file)
        img = Image.open(img_path).resize((70, 50), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        container = tk.Frame(language_frame, bg="#4A646C")
        container.pack(side="left", padx=20)
        tk.Radiobutton(container, image=img, variable=selected_language, value=lang, indicatoron=False,
                       bg="#4A646C", borderwidth=0).pack()
        container.image = img
        
    # Play Button
    play_path = os.path.join(ASSETS_DIR, "play.png")
    play_img = Image.open(play_path).resize((250, 150), Image.Resampling.LANCZOS)
    play_img = ImageTk.PhotoImage(play_img)
    tk.Button(main_container, image=play_img, command=start_game, bg="#4A646C", borderwidth=0).pack(pady=20)
    main_menu_root.image = play_img  # Prevent garbage collection
    
    # Corner Images
    corner_left_path = os.path.join(ASSETS_DIR, "corner_left.png")
    corner_right_path = os.path.join(ASSETS_DIR, "corner_right.png")

    corner_left = Image.open(corner_left_path).resize((100, 100), Image.Resampling.LANCZOS)
    corner_right = Image.open(corner_right_path).resize((100, 100), Image.Resampling.LANCZOS)

    corner_left_img = ImageTk.PhotoImage(corner_left)
    corner_right_img = ImageTk.PhotoImage(corner_right)

    tk.Label(main_menu_root, image=corner_left_img, bg="#4A646C").place(x=20, y=main_menu_root.winfo_screenheight() - 120)
    tk.Label(main_menu_root, image=corner_right_img, bg="#4A646C").place(x=main_menu_root.winfo_screenwidth() - 120, y=main_menu_root.winfo_screenheight() - 120)

    # Keep references to avoid garbage collection
    main_menu_root.corner_left_img = corner_left_img
    main_menu_root.corner_right_img = corner_right_img

    main_menu_root.mainloop()

if __name__ == "__main__":
    main_menu()
