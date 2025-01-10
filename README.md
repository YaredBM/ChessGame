# GameProgramming02Sem
AI Edge	Josue David Pavón Maldonado	93116997<br>
AI Edge	Yáred Iessé Bustillo Medina	56963128<br>
AI Edge	Jonathan David Concha Matas	85876200

# Chess Game Implementation with Python and Tkinter

# Brief Explanation of Chess and Tkinter

# Chess Logic:  
Chess is a strategy game where two players move pieces on an 8x8 grid. The goal is to checkmate the opponent's king. This project focuses on the basic chess rules with checkmate being the only special condition to win the game. The movement of pieces is standard:

- **Pawns** move forward but capture diagonally.
- **Rooks** move horizontally or vertically.
- **Knights** move in an "L" shape.
- **Bishops** move diagonally.
- **Queens** combine the movements of rooks and bishops.
- **Kings** move one square in any direction.

# Tkinter:  
Tkinter is the standard GUI library for Python. It is used to create windowed applications with buttons, labels, canvases, and other elements. For this project, Tkinter will be used to display the chessboard, pieces, and menus while processing user interactions such as selecting and moving pieces.

# Project Overview

In this project, we’re developing a chess game using Python and Tkinter, combining basic chess mechanics with a simple, interactive graphical interface. Tkinter will handle the window, buttons, and other visual elements, while Python will manage the game logic, ensuring a smooth and enjoyable experience for players.

# Setting Up Tkinter

Tkinter will allow us to handle the graphics and input events. It will display the chessboard, pieces, and menus while enabling user interaction via mouse or keyboard.

# Customizable Chessboard

We will set up the chessboard as an 8x8 grid using Tkinter’s `Canvas` widget. Players can customize the colors of the squares, making the game feel more personalized without affecting the core gameplay.

# Representing the Chess Pieces

Each chess piece will be represented by an image, loaded onto the chessboard using Tkinter. Internally, we will use a 2D list to track the positions of the pieces.

# Game Logic

- **Piece movements**: Each piece follows its standard movement.
- **Turn-based gameplay**: Players take turns moving one piece at a time, with valid moves for each piece.
- **Game ending**: The game ends when a player checkmates the opponent’s king.

# User Interaction

- **Mouse**: Select and move pieces by clicking on them and dragging them to new squares.
- **Keyboard**: Players can type in moves using chess notation, such as E2-E4.
- **Voice**: Voice recognition allows players to issue commands like “Move the pawn from E2 to E4.”
- **Text input**: Players can type their moves directly into a text input field.

# Game Modes

- **Player vs Player**: Two players take turns on the same device.
- **Player vs AI**: The player competes against a computer opponent that follows basic decision-making strategies.

# Game End

The game ends when a player checkmates the opponent’s king.

# Class Implementations

The main classes for this game will include:

- **ChessGame**: Manages the game flow, tracks the board state, alternates turns, and checks for checkmate conditions.
- **Board**: Handles the layout of the chessboard and manages the positions of the pieces.
- **Piece**: The base class for all chess pieces, containing attributes like color and position, and defining the basic movement logic for each piece.
- **Specific piece classes (Pawn, Knight, Rook, etc.)**: These classes inherit from `Piece` and define the movement logic for each type of piece.
- **Player**: Handles player actions, whether by mouse, keyboard, or voice, and processes their moves.
- **AI**: Implements the AI logic, allowing the computer to make simple strategic decisions.
- **InputHandler**: Manages all types of input from the user (mouse, keyboard, voice).
- **UI**: Responsible for drawing the board, pieces, menus, and game messages to the screen using Tkinter.

# Visual Design

# Main Menu

The main menu allows players to customize their gameplay experience with the following options:

- # Game Mode Selection:
  - 1 vs 1: Two players compete on the same device.
  - 1 vs AI: A single player faces an AI opponent.
  - Modes are represented with buttons or icons.
  
- # Style Customization:
  - Choose from four unique chessboard themes: Baby (bright and playful), Wood (classic wooden design), Spooky (dark and mysterious), and Nightly (sleek, modern aesthetic).
  
- # Language Options:  
  - Supported languages: English, Spanish, and Turkish.
  - Players can select their preferred language using flag icons or dropdown menus.

# In-Game Interface

- # Interactive Gameplay:
  - Multiple input methods:
    - Mouse: Traditional click-to-select and move functionality.
    - Voice Assistance: Players can give commands like “Move A2 to A4,” and the system will prompt for confirmation: “Are you sure you want to move A2 to A4?”
    - Keyboard Instructions: Players can input moves using specific keyboard commands, providing an alternative to voice and mouse interaction.
  
  - The game highlights valid moves when a piece is selected, ensuring clarity during gameplay.

- # Turn Indication:  
  - Turns are displayed in the format `(1. W1 ; B2.)`, where:
    - `W` represents White’s move.
    - `B` represents Black’s move.
    - The number indicates the turn sequence.

- # Top Menu Bar:
  - The top of the game window includes a menu bar with these options:
    - Home: Return to the game’s main interface.
    - Main Menu: Navigate back to the main menu for customization or to start a new game.
    - Game Rules: Access detailed chess rules and gameplay instructions.
    - Exit: Close the game.

# Modern Aesthetic

The chessboard styles and pieces will adapt to the selected theme, ensuring a visually engaging experience. Tkinter’s features allow for easy customization of colors, fonts, and images to match the selected theme.

# Game Rules Window

The game includes a dedicated **Game Rules Window**, accessible from the top menu bar. This window provides:

- **General Rules**: Explains the objective of the game and turn-based gameplay.
- **How Each Piece Moves**: Detailed descriptions of movement for pawns, rooks, knights, bishops, queens, and kings.
- **Additional Concepts**: Key chess concepts like check, checkmate, stalemate, and draw conditions.

All game rules are available in the three supported languages: English, Spanish, and Turkish.

# Features and Customizations

- **Cross-Language Support**: Players can switch between English, Spanish, and Turkish seamlessly.
- **Customizable Board Styles**: Choose from four unique themes to suit your preferences.
- **Multiple Input Methods**: Play using mouse, voice commands, or keyboard instructions.
- **Dynamic Visuals**: The game highlights valid moves and updates themes based on player preferences.

## Chess Game Main Menu Implementation

This script is responsible for creating the main menu of the chess game. It provides players with an interactive and visually appealing 
interface to customize their gameplay experience. The main menu allows players to configure game settings such as game mode, board 
style, and language before starting the game.

Features

1. Game Mode Selection:

Players can choose between:
- 1 vs 1: Two players compete on the same device.
- 1 vs AI: A single player competes against an AI opponent.

Each mode is represented by an image for easy selection.

2. Style Customization:

Players can select from four unique chessboard styles:
- Baby: A bright and playful design.
- Wood: A classic wooden look.
- Spooky: A dark and mysterious theme.
- Nightly: A sleek and modern aesthetic.

Styles are shown with preview images, allowing players to visualize their choice.

3. Language Selection:

The game supports three languages:
- English
- Spanish
- Turkish

Players can select their preferred language by clicking on flag icons.

4. Start Game Functionality:

Once all selections are made, clicking the "Play" button launches the chess game script (Chess_copy.pyw).

If any selection is missing, a warning message prompts the player to complete the required choices.

5. Enhanced User Interface:

The menu is designed to be fullscreen and uses a consistent theme (#4A646C as the background color) to ensure a polished appearance.

Decorative corner images and responsive button designs enhance the overall user experience.


How the Code Works

1. Asset Management:
- Images for game modes, board styles, and languages are loaded dynamically from the assets folder. File paths are handled using the os
module to ensure compatibility across different operating systems.

2. Interactive Widgets:
- The menu uses Tkinter widgets such as Radiobutton, Label, and Frame to create a clean and interactive layout.
- Buttons are configured to display images, making the interface intuitive and visually engaging.

3. Error Handling:
- The start_game function ensures that players cannot start the game without selecting all required options (mode, style, and
language). Missing selections trigger a popup warning using a messagebox.

4. Launching the Game:
- Once selections are complete, the start_game function closes the main menu and launches the chess game (Chess_copy.pyw) using
subprocess.Popen.


Functions

1. start_game()
- This function is called when the "Play" button is clicked. It validates the player's selections and launches the chess game:

code: 

    def start_game():
        if not selected_mode.get() or not selected_style.get() or not selected_language.get():
            tk.messagebox.showwarning("Missing Selection", "Please select mode, style, and language before starting!")
            return
        main_menu_root.destroy()
        subprocess.Popen(["python", CHESS_COPY_PATH])

Key Details:
- Ensures all options (mode, style, language) are selected. Missing selections prompt a warning.
- Closes the current menu and starts the game script using subprocess.


2. main_menu()
- This function creates and displays the main menu window, allowing players to select game settings:

Code: 

    def main_menu():
        global main_menu_root, selected_mode, selected_style, selected_language # Create and display the main menu.
        main_menu_root = tk.Tk()
        main_menu_root.title("Welcome to Chess")
        main_menu_root.state("zoomed") # Fullscreen
        selected_mode, selected_style, selected_language = tk.StringVar(), tk.StringVar(), tk.StringVar()     
        main_menu_root.mainloop() # GUI setup for game mode, style, and language options...


Key Details:
- Initializes the main menu as a fullscreen window.
- Stores player selections in selected_mode, selected_style, and selected_language variables.
- Runs the menu in a loop to handle user interactions.


3. if __name__ == "__main__": main_menu()
- This statement ensures that the script launches the main menu only when it is executed directly:

Code:

    if __name__ == "__main__":
        main_menu()


Key Details:
- When the script is run directly (e.g., python MainMenu.pyw), it calls the main_menu() function to display the menu interface.
- If the script is imported into another module, this block is skipped, preventing the menu from launching automatically.


Technologies Used

1. Tkinter: Used for creating the graphical interface and handling user interactions.

2. Pillow (PIL): Resizes images for buttons and visual elements.

3. Subprocess: Launches the chess game script in a new process.

4. OS Module: Dynamically constructs file paths for compatibility across operating systems.
