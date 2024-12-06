import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess

# Define base paths for assets
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CHESSBOARDS_DIR = os.path.join(ASSETS_DIR, "images", "Chessboards")
LANGUAGES_DIR = os.path.join(ASSETS_DIR, "images", "Languages")
GENERAL_IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
CHESS_COPY_PATH = os.path.join(BASE_DIR, "Chess_copy.pyw")

def start_game():
    """Start the chess game by closing the main menu and opening Chess_copy.pyw."""
    if not selected_mode.get() or not selected_style.get() or not selected_language.get():
        tk.messagebox.showwarning("Missing Selection", "Please select mode, style, and language before starting!")
        return

    main_menu_root.destroy()  # Close the main menu
    # Launch Chess_copy.pyw
    subprocess.Popen(["python", CHESS_COPY_PATH])

def main_menu():
    """Create and display the main menu."""
    global main_menu_root, selected_mode, selected_style, selected_language

    main_menu_root = tk.Tk()
    main_menu_root.title("Welcome to Chess")
    main_menu_root.state("zoomed")  # Fullscreen
    main_menu_root.configure(bg="#4A646C")  # Set background color

    # Initialize StringVars for selections
    selected_mode = tk.StringVar()
    selected_style = tk.StringVar()
    selected_language = tk.StringVar()

    # Main container for menu options
    main_container = tk.Frame(main_menu_root, bg="#4A646C")
    main_container.pack(pady=30)

    # Welcome text
    welcome_label = tk.Label(
        main_container,
        text="Welcome to Chess",
        font=("Arial", 36, "bold"),
        bg="#4A646C",
        fg="white",
    )
    welcome_label.pack(pady=10)

    # Game mode selection
    mode_label = tk.Label(
        main_container,
        text="Choose your game mode:",
        font=("Arial", 18, "bold"),
        bg="#4A646C",
        fg="white",
    )
    mode_label.pack(pady=5)

    mode_frame = tk.Frame(main_container, bg="#4A646C")
    mode_frame.pack(pady=5)

    # Load images for game modes
    mode_images = {
        "1 VS 1": os.path.join(GENERAL_IMAGES_DIR, "1vs1.png"),
        "1 VS AI": os.path.join(GENERAL_IMAGES_DIR, "1vsAI.png"),
    }
    for mode, path in mode_images.items():
        img = Image.open(path).resize((150, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        button = tk.Radiobutton(
            mode_frame,
            image=img,
            variable=selected_mode,
            value=mode,
            bg="#4A646C",
            indicatoron=False,
            selectcolor="#4A646C",
        )
        button.image = img
        button.pack(side="left", padx=20)

    # Style selection
    style_label = tk.Label(
        main_container,
        text="Choose your style:",
        font=("Arial", 18, "bold"),
        bg="#4A646C",
        fg="white",
    )
    style_label.pack(pady=5)

    style_frame = tk.Frame(main_container, bg="#4A646C")
    style_frame.pack(pady=5)

    styles = [("Baby", "baby.png"), ("Wood", "wood.png"), ("Spooky", "spooky.png"), ("Nightly", "nightly.png")]

    for style_name, style_image in styles:
        img = Image.open(os.path.join(CHESSBOARDS_DIR, style_image)).resize((80, 80), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        style_container = tk.Frame(style_frame, bg="#4A646C")
        style_container.pack(side="left", padx=10)

        tk.Radiobutton(
            style_container,
            image=img,
            variable=selected_style,
            value=style_name,
            bg="#4A646C",
            indicatoron=False,
            selectcolor="#4A646C",
        ).pack()

        style_container.image = img
        label = tk.Label(
            style_container,
            text=style_name,
            font=("Arial", 14),
            bg="#4A646C",
            fg="white",
        )
        label.pack()

    # Language selection
    language_label = tk.Label(
        main_container,
        text="Choose your language:",
        font=("Arial", 18, "bold"),
        bg="#4A646C",
        fg="white",
    )
    language_label.pack(pady=5)

    language_frame = tk.Frame(main_container, bg="#4A646C")
    language_frame.pack(pady=5)

    languages = [("Spanish", "spanish.png"), ("English", "english.png"), ("Turkish", "turkish.png")]

    for language_name, language_flag in languages:
        img = Image.open(os.path.join(LANGUAGES_DIR, language_flag)).resize((80, 50), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        lang_container = tk.Frame(language_frame, bg="#4A646C")
        lang_container.pack(side="left", padx=10)

        tk.Radiobutton(
            lang_container,
            image=img,
            variable=selected_language,
            value=language_name,
            bg="#4A646C",
            indicatoron=False,
            selectcolor="#4A646C",
        ).pack()

        lang_container.image = img
        label = tk.Label(
            lang_container,
            text=language_name,
            font=("Arial", 14),
            bg="#4A646C",
            fg="white",
        )
        label.pack()

    # Play button (image)
    play_image_path = os.path.join(GENERAL_IMAGES_DIR, "play.png")
    play_image = Image.open(play_image_path).resize((200, 150), Image.Resampling.LANCZOS)
    play_photo = ImageTk.PhotoImage(play_image)

    play_button = tk.Button(
        main_container,
        image=play_photo,
        command=start_game,
        bg="#4A646C",
        relief="flat",
    )
    play_button.image = play_photo
    play_button.pack(pady=5)

    # Add corner images
    corner_left_path = os.path.join(GENERAL_IMAGES_DIR, "corner_left.png")
    corner_right_path = os.path.join(GENERAL_IMAGES_DIR, "corner_right.png")

    corner_left = Image.open(corner_left_path).resize((80, 80), Image.Resampling.LANCZOS)
    corner_left_photo = ImageTk.PhotoImage(corner_left)
    corner_left_label = tk.Label(main_menu_root, image=corner_left_photo, bg="#4A646C")
    corner_left_label.place(x=10, y=main_menu_root.winfo_screenheight() - 100)

    corner_right = Image.open(corner_right_path).resize((80, 80), Image.Resampling.LANCZOS)
    corner_right_photo = ImageTk.PhotoImage(corner_right)
    corner_right_label = tk.Label(main_menu_root, image=corner_right_photo, bg="#4A646C")
    corner_right_label.place(x=main_menu_root.winfo_screenwidth() - 100, y=main_menu_root.winfo_screenheight() - 100)

    # Keep references to images
    main_menu_root.corner_left_photo = corner_left_photo
    main_menu_root.corner_right_photo = corner_right_photo

    # Run the main menu
    main_menu_root.mainloop()


if __name__ == "__main__":
    main_menu()
