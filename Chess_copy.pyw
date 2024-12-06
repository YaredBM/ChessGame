import tkinter as tk
from tkinter import messagebox
import string #for a string to store alphabet
import os, sys #help with importing images
from PIL import Image, ImageTk #help with implementing images into GUI
from PIL.ImageTk import PhotoImage
from tkinter import filedialog
import pickle


BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
WHITE_DIR = os.path.join(ASSETS_DIR, "images", "White")
BLACK_DIR = os.path.join(ASSETS_DIR, "images", "Black")

class Board(tk.Frame):
    def __init__(self, parent, length, width):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.length = length
        self.width = width

        # Left panel for the menu button
        self.left_panel = tk.Frame(self.parent, bg="gray", width=100)
        self.left_panel.pack(side="left", fill="y")

        self.left_button = tk.Button(
            self.left_panel,
            text="Menu",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            command=self.menu_action
        )
        self.left_button.pack(padx=10, pady=10, anchor="nw")

        # Main chessboard frame
        self.board_frame = tk.Frame(self.parent, bg="white", width=800, height=800)
        self.board_frame.pack(side="left", fill="none", expand=True)

        # Right panel for the turn label
        self.right_panel = tk.Frame(self.parent, bg="gray", width=200)
        self.right_panel.pack(side="right", fill="y")

        self.turn_label = tk.Label(
            self.right_panel,
            text="WHITE'S TURN",
            font=("Arial", 16, "bold"),
            bg="gray",
            fg="white",
            width=15,
            height=3,
            borderwidth=5,
            relief="raised"
        )
        self.turn_label.pack(pady=50)

        # Other initializations
        self.squares = {}
        self.ranks = string.ascii_lowercase[:8]
        self.white_images = {}
        self.black_images = {}
        self.buttons_pressed = 0
        self.turns = 0
        self.sq1 = None
        self.sq2 = None
        self.sq1_button = None
        self.sq2_button = None
        self.piece_color = None
        self.highlighted_squares = []

        self.set_squares()

    def menu_action(self):
        """Placeholder function for the menu button."""
        messagebox.showinfo("Menu", "Menu button clicked!")

    def update_turn_label(self):
        """Updates the turn label to reflect the current player's turn."""
        current_turn = "WHITE'S TURN" if self.turns % 2 == 0 else "BLACK'S TURN"
        self.turn_label.config(text=current_turn)

    def select_piece(self, button):
        current_turn_color = "white" if self.turns % 2 == 0 else "black"

        # Compare image IDs as strings
        if str(button["image"]) in [str(image) for image in self.white_pieces]:
            piece_color = "white"
        elif str(button["image"]) in [str(image) for image in self.black_pieces]:
            piece_color = "black"
        else:
            piece_color = None

        # Debugging Information
        print(f"DEBUG: Button Image ID: {button['image']}")
        print(f"DEBUG: White Pieces Image IDs: {[str(image) for image in self.white_pieces]}")
        print(f"DEBUG: Black Pieces Image IDs: {[str(image) for image in self.black_pieces]}")
        print(f"DEBUG: Current Turn Color: {current_turn_color}")
        print(f"DEBUG: Detected Piece Color: {piece_color}")

        # First click: Select a piece
        if self.buttons_pressed == 0:
            if piece_color == current_turn_color:
                self.piece_color = piece_color
                self.sq1 = list(self.squares.keys())[list(self.squares.values()).index(button)]
                self.sq1_button = button
                self.buttons_pressed = 1
            else:
                messagebox.showwarning("Invalid Selection", "You must select your own piece.")
        elif self.buttons_pressed == 1:
            # Second click logic remains unchanged
            self.sq2 = list(self.squares.keys())[list(self.squares.values()).index(button)]
            self.sq2_button = button

            if self.sq2 == self.sq1:
                self.buttons_pressed = 0
                return

            if self.allowed_piece_move() and not self.friendly_fire():
                self.squares[self.sq2].config(image=self.sq1_button["image"])
                self.squares[self.sq2].image = self.sq1_button["image"]
                self.squares[self.sq1].config(image=self.white_images["blank.png"])
                self.squares[self.sq1].image = self.white_images["blank.png"]

                self.turns += 1
                self.update_turn_label()
            else:
                messagebox.showwarning("Invalid Move", "This move is not allowed.")

            self.buttons_pressed = 0



            
    def promotion_menu(self, color): #creates menu to choose what piece to change the pawn to
        def return_piece(piece): #function called by buttons to make the change and destroy window
            self.squares[self.sq2].config(image=piece)
            self.squares[self.sq2].image = piece
            promo.destroy()
            return
        
        promo = tk.Tk() #creates a new menu with buttons depending on pawn color
        promo.title("Choose what to promote your pawn to")
        if color=="white":
            promo_knight = tk.Button(promo, text="Knight", command=lambda: return_piece("pyimage4")) #triggers return_piece function when selected
            promo_knight.grid(row=0, column=0)
            promo_bishop = tk.Button(promo, text="Bishop", command=lambda: return_piece("pyimage1"))
            promo_bishop.grid(row=0, column=1)
            promo_rook = tk.Button(promo, text="Rook", command=lambda: return_piece("pyimage7"))
            promo_rook.grid(row=1, column=0)
            promo_queen = tk.Button(promo, text="Queen", command=lambda: return_piece("pyimage6"))
            promo_queen.grid(row=1, column=1)
        elif color=="black":
            promo_knight = tk.Button(promo, text="Knight", command=lambda: return_piece("pyimage11"))
            promo_knight.grid(row=0, column=0)
            promo_bishop = tk.Button(promo, text="Bishop", command=lambda: return_piece("pyimage8"))
            promo_bishop.grid(row=0, column=1)
            promo_rook = tk.Button(promo, text="Rook", command=lambda: return_piece("pyimage14"))
            promo_rook.grid(row=1, column=0)
            promo_queen = tk.Button(promo, text="Queen", command=lambda: return_piece("pyimage13"))
            promo_queen.grid(row=1, column=1)
        promo.mainloop()
        return
            
    def friendly_fire(self):
        """Prevent capturing own pieces."""
        piece_2_color = self.sq2_button["image"]

        # Check if the piece on sq2 belongs to the current player
        if self.piece_color == "white" and piece_2_color in self.white_images.values():
            return True
        if self.piece_color == "black" and piece_2_color in self.black_images.values():
            return True
        return False

        
    def clear_path(self, piece): #makes sure that the squares in between sq1 and sq2 aren't occupied
        if piece == "rook" or piece == "queen":   
            if self.sq1[0] == self.sq2[0]: #for vertical movement
                pos1 = min(int(self.sq1[1]), int(self.sq2[1]))
                pos2 = max(int(self.sq1[1]), int(self.sq2[1]))
                for i in range(pos1+1, pos2):
                    square_on_path = self.squares[self.sq1[0]+str(i)].cget("image")
                    if square_on_path != "pyimage2":
                        return False
                    
            elif self.sq1[1] == self.sq2[1]: #for horizontal movement
                pos1 = min(self.ranks.find(self.sq1[0]), self.ranks.find(self.sq2[0]))
                pos2 = max(self.ranks.find(self.sq1[0]), self.ranks.find(self.sq2[0]))

                for i in range(pos1+1, pos2):
                    square_on_path = self.squares[self.ranks[i]+self.sq1[1]].cget("image")
                    if square_on_path != "pyimage2":
                        return False
                    
        if piece == "bishop" or piece == "queen": #for diagonal movement
            x1 = self.ranks.find(self.sq1[0])
            x2 = self.ranks.find(self.sq2[0])
            y1 = int(self.sq1[1])
            y2 = int(self.sq2[1])
            
            if  y1<y2:
                if x1<x2: #NE direction
                    for x in range(x1+1, x2):
                        y1 += 1
                        square_on_path = self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path != "pyimage2":
                            return False
                elif x1>x2: #NW direction
                    for x in range(x1-1, x2, -1):
                        y1 += 1
                        square_on_path = self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path != "pyimage2":
                            return False
            elif y1>y2:
                if x1<x2: #SE direction
                    for x in range(x1+1, x2):
                        y1 -= 1
                        square_on_path = self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path != "pyimage2":
                            return False
                if x1>x2: #SW direction
                    for x in range(x1-1, x2, -1):
                        y1 -= 1
                        square_on_path = self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path != "pyimage2":
                            return False
        return True
                
        
    def allowed_piece_move(self): #checks whether the piece can move to square 2 with respect to their movement capabilities
        wb, wk, wn, wp, wq, wr = "pyimage1", "pyimage3", "pyimage4", "pyimage5", "pyimage6", "pyimage7" #redefining pyimages for readability
        bb, bk, bn, bp, bq, br = "pyimage8", "pyimage10", "pyimage11", "pyimage12", "pyimage13", "pyimage14"

        if self.sq1_button["image"] == "pyimage2" or self.sq1_button["image"] == "pyimage9": #for when this function is called for check
            return False
        
        if (self.sq1_button["image"] == wb or self.sq1_button["image"] == bb) and self.clear_path("bishop"): #bishop movement        
            if abs(int(self.sq1[1]) - int(self.sq2[1])) == abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0])): #makes sure there is equal change between file and rank movement
                return True

        if self.sq1_button["image"] == wn or self.sq1_button["image"] == bn: #knight movement
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) == 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0])) == 1): #allows tall L moves
                return True
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) == 1) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0])) == 2): #allows wide L moves
                return True
        
        if self.sq1_button["image"] == wk or self.sq1_button["image"] == bk: #king movement
            if (abs(int(self.sq1[1]) - int(self.sq2[1])) < 2) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) < 2: #allows 1 square moves
                return True
            if self.castle() is True:
                return True
        
        if self.sq1_button["image"] == wp: #white pawn movement
            if "2" in self.sq1: #allows for 2 space jump from starting pos
                if (int(self.sq1[1])+1 == int(self.sq2[1]) or int(self.sq1[1])+2 == int(self.sq2[1])) and self.sq1[0] == self.sq2[0] and self.sq2_button["image"] == "pyimage2": #allows 2 sq movement
                    in_front = self.squares[self.sq1[0] + str(int(self.sq1[1])+1)]
                    if in_front["image"] == "pyimage2": #makes sure that there is no piece blocking path
                        return True
            if int(self.sq1[1])+1 == int(self.sq2[1]) and self.sq1[0] == self.sq2[0] and self.sq2_button["image"] == "pyimage2": #allows 1 sq movement
                    return True
            if int(self.sq1[1])+1 == int(self.sq2[1]) and (abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0]))) == 1 and self.sq2_button["image"] != "pyimage2": #allows the capturing of diagonal pieces
                    return True

                
        if self.sq1_button["image"] == bp: #black pawn movement
            if "7" in self.sq1: #allows for 2 space jump from starting pos
                if (int(self.sq1[1]) == int(self.sq2[1])+1 or int(self.sq1[1]) == int(self.sq2[1])+2) and self.sq1[0] == self.sq2[0] and self.sq2_button["image"] == "pyimage2": #only allows it to move straight 1 or 2 sq
                    return True
            if int(self.sq1[1]) == int(self.sq2[1])+1 and self.sq1[0] == self.sq2[0] and self.sq2_button["image"] == "pyimage2":
                    return True
            if int(self.sq1[1]) == int(self.sq2[1])+1 and abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0])) == 1 and self.sq2_button["image"] != "pyimage2": #allows the capturing of diagonal pieces if there is an opponent piece there
                    return True

        if (self.sq1_button["image"] == wq or self.sq1_button["image"] == bq) and self.clear_path("queen"): #queen movement
            if int(self.sq1[1]) == int(self.sq2[1]) or self.sq1[0] == self.sq2[0]: #only allows movement within same rank or file
                return True
            if abs(int(self.sq1[1]) - int(self.sq2[1])) == abs(self.ranks.find(self.sq1[0]) - self.ranks.find(self.sq2[0])):
                return True
        
        if self.sq1_button["image"] == wr or self.sq1_button["image"] == br: #rook movement
            if (int(self.sq1[1]) == int(self.sq2[1]) or self.sq1[0] == self.sq2[0]) and self.clear_path("rook"): #only allows movement within same rank or file
                return True  
        return False
    
    def castle(self): #checks to see if the move entails a castle, and if a castle is allowed
        if self.wk_moved == False: #makes sure king hasn't moved
            if self.wr1_moved == False and self.sq2 == "c1": #finds out which way user wants to castle and if the rook has moved (in this case white would want to castle to the left)
                for x in range(1,4): #checks to see if squares in between rook and king are empty and are not a possible move for opponent
                    square_button = self.squares[self.ranks[x]+str(1)]
                    if square_button["image"] != "pyimage2":
                        return False
                    self.squares["a1"].config(image="pyimage2")
                    self.squares["a1"].image = "pyimage2"
                    self.squares["d1"].config(image="pyimage7")
                    self.squares["d1"].image = ("pyimage7")
                    self.castled = True
                    return True
            if self.wr2_moved == False and self.sq2 == "g1":
                for x in range(5,7): #checks to see if squares in between rook and king are empty and are not a possible move for opponent
                    square_button = self.squares[self.ranks[x]+str(1)]
                    if square_button["image"] != "pyimage2":
                        return False
                    self.squares["h1"].config(image="pyimage2")
                    self.squares["h1"].image = "pyimage2"
                    self.squares["f1"].config(image="pyimage7")
                    self.squares["f1"].image = ("pyimage7")
                    self.castled = True
                    return True
        if self.bk_moved == False:
            if self.br1_moved == False and self.sq2 == "c8":
                for x in range(1,3): #checks to see if squares in between rook and king are empty and are not a possible move for opponent
                    square_button = self.squares[self.ranks[x]+str(8)]
                    if square_button["image"] != "pyimage2":
                        return False
                    self.squares["a8"].config(image="pyimage2")
                    self.squares["a8"].image = "pyimage2"
                    self.squares["d8"].config(image="pyimage14")
                    self.squares["d8"].image = ("pyimage14")
                    self.castled = True
                    return True
            if self.br2_moved == False and self.sq2 == "g8":
                for x in range(5,7): #checks to see if squares in between rook and king are empty and are not a possible move for opponent
                    square_button = self.squares[self.ranks[x]+str(8)]
                    if square_button["image"] != "pyimage2":
                        return False
                    self.squares["h8"].config(image="pyimage2")
                    self.squares["h8"].image = "pyimage2"
                    self.squares["f8"].config(image="pyimage14")
                    self.squares["f8"].image = ("pyimage14")
                    self.castled = True
                    return True
        else:
            return False
   
        self.bk_moved = False
        self.wr1_moved = False
        self.wr2_moved = False
        self.br1_moved = False
        self.br2_moved = False

    def in_check(self): #prevents a move if king is under attack
        previous_sq1 = self.sq1 #stores current values assigned to values
        previous_sq1_button = self.sq1_button
        previous_sq2 = self.sq2
        previous_sq2_button = self.sq2_button
        
        def return_previous_values():
            self.sq1 = previous_sq1
            self.sq1_button = previous_sq1_button
            self.sq2 = previous_sq2
            self.sq2_button = previous_sq2_button
            
        if self.piece_color == "white":
            self.sq2 = self.find_king("pyimage3") #calls find_king function to find pos of king
            for key in self.squares: #iterates through each square
                self.sq1 = key
                self.sq1_button = self.squares[self.sq1]
                if self.sq1_button["image"] in self.black_pieces:
                    if self.allowed_piece_move(): #checks to see if the king's current pos is a possible move for the piece
                        return True
        if self.piece_color == "black":
            self.sq2 = self.find_king("pyimage10")
            for key in self.squares:
                self.sq1 = key
                self.sq1_button = self.squares[self.sq1] 
                if self.sq1_button["image"] in self.white_pieces:
                    if self.allowed_piece_move():
                        return True
        return_previous_values()
        return False
    
    def find_king(self, king): #finds the square where the king is currently on
        for square  in self.squares:
            button = self.squares[square]
            if button["image"] == king:
                return square
    
    def set_squares(self):
        """Creates the chessboard buttons and adds them to the grid."""
        for x in range(8):
            for y in range(8):
                square_color = "tan4" if (x + y) % 2 == 0 else "burlywood1"
                B = tk.Button(self.board_frame, bg=square_color, activebackground="lawn green")
                B.grid(row=8 - x, column=y)
                pos = self.ranks[y] + str(x + 1)
                self.squares[pos] = B
                self.squares[pos].config(command=lambda key=self.squares[pos]: self.select_piece(key))        
        
    def import_pieces(self):
        for path, image_dict in [(WHITE_DIR, self.white_images), (BLACK_DIR, self.black_images)]:
            for file in os.listdir(path):
                img = Image.open(os.path.join(path, file)).resize((80, 80), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(image=img)
                image_dict[file] = img

        # Populate white_pieces and black_pieces with references to loaded images
        self.white_pieces = [self.white_images[piece] for piece in ["b.png", "k.png", "n.png", "p.png", "q.png", "r.png"]]
        self.black_pieces = [self.black_images[piece] for piece in ["b.png", "k.png", "n.png", "p.png", "q.png", "r.png"]]



    def set_pieces(self):
        """Places chess pieces in their initial positions."""
        white_rank1 = {"a1": "r.png", "b1": "n.png", "c1": "b.png", "d1": "q.png", "e1": "k.png", 
                    "f1": "b.png", "g1": "n.png", "h1": "r.png"}
        white_rank2 = {"a2": "p.png", "b2": "p.png", "c2": "p.png", "d2": "p.png", "e2": "p.png", 
                    "f2": "p.png", "g2": "p.png", "h2": "p.png"}
        black_rank8 = {"a8": "r.png", "b8": "n.png", "c8": "b.png", "d8": "q.png", "e8": "k.png", 
                    "f8": "b.png", "g8": "n.png", "h8": "r.png"}
        black_rank7 = {"a7": "p.png", "b7": "p.png", "c7": "p.png", "d7": "p.png", "e7": "p.png", 
                    "f7": "p.png", "g7": "p.png", "h7": "p.png"}

        # Assign white pieces
        for pos, piece in white_rank1.items():
            self.squares[pos].config(image=self.white_images[piece])
            self.squares[pos].image = self.white_images[piece]
        for pos, piece in white_rank2.items():
            self.squares[pos].config(image=self.white_images[piece])
            self.squares[pos].image = self.white_images[piece]

        # Assign black pieces
        for pos, piece in black_rank8.items():
            self.squares[pos].config(image=self.black_images[piece])
            self.squares[pos].image = self.black_images[piece]
        for pos, piece in black_rank7.items():
            self.squares[pos].config(image=self.black_images[piece])
            self.squares[pos].image = self.black_images[piece]

        # Assign blank images to remaining squares
        blank_piece = "blank.png"
        for rank in range(3, 7):  # Empty ranks
            for file in self.ranks:
                pos = f"{file}{rank}"
                self.squares[pos].config(image=self.white_images[blank_piece])  # Use blank white square
                self.squares[pos].image = self.white_images[blank_piece]


# Functionality for the menu options
def home_action():
    root.destroy()
    messagebox.showinfo("Home", "Welcome to the Chess Game!")
    os.startfile(os.path.join(os.path.dirname(__file__), "MainMenu.pyw"))

def save_game_action():
    # Get the file path from the user
    file_path = filedialog.asksaveasfilename(
        title="Save Game",
        defaultextension=".pkl",
        filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")]
    )
    if file_path:  # Proceed only if the user provides a valid path
        game_state = {"pieces": {}, "turns": board.turns}
        for pos, button in board.squares.items():
            game_state["pieces"][pos] = button["image"]
        with open(file_path, "wb") as file:
            pickle.dump(game_state, file)
        messagebox.showinfo("Save Game", "Game has been saved!")

def load_game_action():
    # Get the file path from the user
    file_path = filedialog.askopenfilename(
        title="Load Game",
        filetypes=[("Pickle Files", "*.pkl"), ("All Files", "*.*")]
    )
    if file_path:  # Proceed only if the user provides a valid path
        try:
            with open(file_path, "rb") as file:
                game_state = pickle.load(file)
            for pos, piece in game_state["pieces"].items():
                board.squares[pos].config(image=piece)
                board.squares[pos].image = piece
            board.turns = game_state["turns"]
            board.turn_label.config(text=f"{'White' if board.turns % 2 == 0 else 'Black'}'s Turn")
            messagebox.showinfo("Load Game", "Game has been loaded!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {e}")


def restart_game_action():
    board.set_pieces()
    board.turns = 0
    board.turn_label.config(text="White's Turn")
    messagebox.showinfo("Restart Game", "Game has been restarted!")

def game_rules_action():
    # Show game rules in a message box
    rules = """Chess Game Rules:
1. The game is played on an 8x8 board.
2. Each piece moves according to its unique rules.
3. The goal is to checkmate the opponent's king.
4. Special moves include castling, en passant, and pawn promotion."""
    messagebox.showinfo("Game Rules", rules)

def exit_action():
    root.quit()

# Create the Tkinter root window
root = tk.Tk()
root.geometry("800x800")
root.state("zoomed")
root.title("Chess Game")

# Create the menu bar
menu_bar = tk.Menu(root)

# Add the "Home" menu
home_menu = tk.Menu(menu_bar, tearoff=0)
home_menu.add_command(label="Home", command=home_action)
menu_bar.add_cascade(label="Home", menu=home_menu)

# Add the "Main Menu" menu with suboptions
main_menu = tk.Menu(menu_bar, tearoff=0)
main_menu.add_command(label="Save Game", command=save_game_action)
main_menu.add_command(label="Load Game", command=load_game_action)
main_menu.add_command(label="Restart Game", command=restart_game_action)
menu_bar.add_cascade(label="Main Menu", menu=main_menu)

# Add the "Game Rules" menu
rules_menu = tk.Menu(menu_bar, tearoff=0)
rules_menu.add_command(label="Game Rules", command=game_rules_action)
menu_bar.add_cascade(label="Game Rules", menu=rules_menu)

# Add the "Exit" menu
exit_menu = tk.Menu(menu_bar, tearoff=0)
exit_menu.add_command(label="Exit", command=exit_action)
menu_bar.add_cascade(label="Exit", menu=exit_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Chess Board Initialization
board = Board(root, 8, 8)
board.import_pieces()
board.set_pieces()

# Start the main loop
root.mainloop()