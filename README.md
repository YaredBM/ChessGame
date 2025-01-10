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

# Game Mode

- **Player vs Player**: Two players take turns on the same device.

# Game End

The game ends when a player checkmates the opponent’s king.

# Class Implementations

The main classes for this game will include:

- **ChessGame**: Manages the game flow, tracks the board state, alternates turns, and checks for checkmate conditions.
- **Board**: Handles the layout of the chessboard and manages the positions of the pieces.
- **Piece**: The base class for all chess pieces, containing attributes like color and position, and defining the basic movement logic for each piece.
- **Specific piece classes (Pawn, Knight, Rook, etc.)**: These classes inherit from `Piece` and define the movement logic for each type of piece.
- **Player**: Handles player actions, whether by mouse, keyboard, or voice, and processes their moves.
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
- 1 vs 1: Two players compete on the same device.
- Player Names Input: Before starting a game, players are prompted to enter their names for personalization.

2. Custom Board Styles:
- Players can choose from multiple board themes:
Baby, Wood, Spooky, Nightly, and Love styles.
- Style previews are displayed via visual icons for easy selection.

3. Language Options:
- Available languages: English, Spanish, and Turkish.

4. Interactive Menu Design:
- Fullscreen display for better immersion.
- Clean, modern UI with responsive design elements.
- Enhanced by visual decorations and user-friendly icons.

Technical Implementation

1. Dynamic Paths:
- The menu dynamically loads images and assets using relative paths, ensuring compatibility across systems.

2. Customizable Gameplay:
- Game configuration (mode, style, and language) is passed directly to the main game logic when the player starts a session.

3. Name Input Window:
- For 1 vs 1 mode, a separate window prompts players for their names.
- Names and preferences are transferred to the main game on launch.

4. Graphical Enhancements:
- Integrated with Pillow (PIL) for image scaling and rendering.
- The menu includes decorative corner images to enhance visual appeal.

How the Code Works

1. Main Menu Initialization (main_menu):

- The program starts by calling the main_menu() function, which creates and displays the main window.
- Tkinter widgets like Frame, Label, and Radiobutton are used to build the user interface for game mode, style, and language selection.
- Image assets are dynamically loaded from a specified directory using relative paths to ensure portability across systems.

2. Game Start Process (start_game):

- Before launching the game, the program checks that all necessary selections (mode, style, and language) are made.
- If selections are incomplete, a warning prompts the player to complete the setup.
- In 1 vs 1 mode, a name input window (get_player_names()) prompts players to enter their names before starting the game.

3. Player Names Input (get_player_names):
- This function dynamically adjusts its interface based on the selected game mode.
- For 1 vs 1 mode, players are prompted to input names for both players.
- The subprocess.Popen() function is used to launch the chess game (Chess.pyw) with the selected configurations.

4. Menu Enhancements:
- Decorative elements like corner images are integrated using ImageTk.PhotoImage.
- Fullscreen mode is achieved with state("zoomed").

Functions and Their Roles

1. main_menu():

- Creates and displays the main menu window.
- Handles UI setup for mode, style, and language selection.
- Manages loading and displaying image assets.

2. start_game():
- Validates that the user has selected game mode, style, and language.
- Launches the chess game with the selected configurations if inputs are complete.
- Calls get_player_names() when player names need to be entered.

3. get_player_names(mode):
- Opens a custom window for entering player names.
- Dynamically adjusts UI based on the selected game mode.
- Passes player names, board style, and language to the game startup process.

## Game Rules Explanation

The create_window_with_pages() function creates a graphical user interface (GUI) application using Python's tkinter library. The application serves as an interactive information display with multiple pages, each containing an image.

Functionality Overview

1. Window Initialization and Centering

- The center_window function ensures that the application window is centered on the screen with a slight upward adjustment.
- The window is set to a fixed size of 900x600 pixels.

2. File Searching

- The find_file_recursive function recursively searches for image files in the project directory and its subdirectories.
- This ensures that the application can locate necessary assets (.png files) even if their exact locations vary.

3. Dynamic Image Loading

- A dictionary, image_files, maps tab names to their corresponding image filenames.
- Using find_file_recursive, the script dynamically locates each image file, storing their paths in the image_paths dictionary.
- If a required file is missing, an error message is printed, and the application exits.

4. Main Window Setup

- A tkinter Tk window is created with a title ("Chess Information") and an icon loaded from the assets/Menu/Chess-Logo.ico directory.

5. Tabbed Interface with ttk.Notebook
- A ttk.Notebook widget creates a tabbed interface, allowing users to switch between pages.
- Each tab corresponds to a specific category (e.g., "General Chess Rules", "Piece Movements").

6. Image Processing and Display
- Each image is resized to fit the window dimensions (900x600 pixels) using Pillow (PIL) with high-quality resizing
(Image.Resampling.LANCZOS).
- A tk.Label widget displays the image, covering the entire tab frame.

7. Garbage Collection Management

- To prevent garbage collection of the images, references are stored in a dictionary and explicitly assigned to the Label widget.

8. Event Loop

- The root.mainloop() call starts the Tkinter event loop, keeping the application window open and responsive.

Use Case

This function is ideal for creating informational applications with an image-based navigation system. The example implementation displays chess-related content, but it can be easily adapted for other purposes by modifying the image_files dictionary.

Key Libraries Used

1. tkinter: For creating the GUI.
2. ttk: Provides a modern-themed tabbed interface (ttk.Notebook).
3. Pillow (PIL): For image manipulation and resizing.
4. os: To handle file paths and directory traversal.

Error Handling

- The script verifies that all required image files are located.
- If a file is missing, an error message is printed, and the program exits gracefully.

## Chess Game Implementation

This class is responsible for setting up and managing the entire chess game. It handles board rendering, piece management, and game
state (including saving and loading). The class provides a GUI with buttons for interaction and labels for displaying game status.

Attributes:

- root: The main Tkinter window that holds the chess game.
- board: The chessboard, which is a grid of 8x8 buttons, each representing a square on the board.
- style_colors: Defines the color scheme for the squares on the board.
- squares: A dictionary that maps each square (e.g., "a1", "h8") to a button.
- white_images and black_images: Dictionaries that store the images for white and black pieces, respectively.
- selected_language: The language currently selected for the interface.
- current_language: A dictionary containing all the text used in the interface, such as button labels, messages, and game information.

Methods:

- find_king(self, king):
Searches for the square where the king piece is currently located by checking the image of each square.

- set_squares(self):
Creates the chessboard with buttons representing squares. The color alternates based on the square's position, and each square is
assigned a button with a click command to select pieces.

- import_pieces(self):
Loads the images for the pieces based on the selected style (white or black pieces) from the corresponding directory.

- set_pieces(self):
Places the pieces in their default starting positions, including pawns, rooks, knights, bishops, queens, and kings. It also fills the remaining squares with blank images.

- home_action():
Action triggered when the "Home" menu item is selected. This closes the current window and opens the main menu.

- save_game_action(board, move_log_label, turn_label, player1_name):
Saves the current game state (board positions, move log, and turn information) to a .pkl file. After saving, the game is automatically restarted.

- load_game_action(board, move_log_label, turn_label):
Loads a previously saved game state from a .pkl file and restores the board, move log, and other relevant game data.

- restart_game(self, move_log_label, turn_label, player1_name):
Restarts the game by resetting the board to the initial positions, clearing the move log, and updating the turn label.

- game_rules_action():
Opens a new window displaying the game rules when the "Game Rules" menu option is selected.

- change_view(mode):
Switches between Light Mode and Dark Mode for the user interface. This affects the background and text colors of various elements.

- exit_action():
Closes the game when the "Exit" menu option is selected.

Menu System:

The menu bar provides several options:

- Home: Opens the home screen.
- Main Menu: Contains options to save, load, and restart the game.
- Game Rules: Displays a window showing the rules of the game.
- Change View: Switch between Light and Dark modes.
- Exit: Closes the game.

User Interface:

- Chessboard: A grid of 8x8 buttons represents the chessboard. Pieces are displayed as images on these buttons.
- Turn Label: Shows the current player's turn.
- Move Log Label: Displays the history of moves made during the game.
- Menu Button: Opens a menu with options for saving, loading, and restarting the game, among others.
