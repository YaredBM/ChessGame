import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_window_with_pages():
    # Function to center the window on the screen, slightly higher
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 50  # Slight adjustment upward
        window.geometry(f"{width}x{height}+{x}+{y}")

    # Function to recursively search for a file in a directory
    def find_file_recursive(start_dir, filename):
        for root, dirs, files in os.walk(start_dir):
            if filename in files:
                return os.path.join(root, filename)
        return None

    # Automatically find image paths from anywhere within the script's directory
    base_directory = os.path.dirname(os.path.abspath(__file__))  # Get the base directory of the script
    image_files = {
        "General Chess Rules": "general_chess_rules.png",
        "Piece Movements": "piece_movements.png",
        "Additional Information": "additional_information.png",
        "About This Game": "about.png",
        "Meet the Team": "team.png",
    }

    # Locate each image file
    image_paths = {}
    for name, filename in image_files.items():
        path = find_file_recursive(base_directory, filename)
        if path is None:
            print(f"Error: File '{filename}' not found in '{base_directory}' or its subdirectories.")
            return
        image_paths[name] = path

    # Create the main window
    root = tk.Tk()
    root.title("Chess Information")
    center_window(root, 900, 600)  # Center the window with the adjustment
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")
    root.iconbitmap(icon_path)

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Load images for each page
    images = {}
    for name, path in image_paths.items():
        img = Image.open(path)
        img = img.resize((900, 600), Image.Resampling.LANCZOS)
        images[name] = ImageTk.PhotoImage(img)

    # Create a frame for each page and add images
    for name, img in images.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=name)  # Add the frame with the appropriate title
        label = tk.Label(frame, image=img)
        label.place(relwidth=1, relheight=1)  # Cover the entire frame
        label.image = img  # Keep a reference to avoid garbage collection

    # Start the Tkinter event loop
    root.mainloop()

# Run the function to create the window with pages
create_window_with_pages()
