import tkinter as tk
from tkinter import messagebox
import string #for a string to store alphabet
import os, sys #help with importing images
from PIL import Image, ImageTk #help with implementing images into GUI
from PIL.ImageTk import PhotoImage
import subprocess  # Make sure subprocess is imported
import pickle
from tkinter import filedialog, messagebox  # Para diálogos de archivos y mensajes
import shutil

player1_name = sys.argv[2] if len(sys.argv) > 2 else "Player 1"
player2_name = sys.argv[3] if len(sys.argv) > 3 else "Player 2"

STYLES = {
    "Wood": ("#503E32", "#A26D4C"),
    "Baby": ("#5D9A75", "#F2E9C0"),
    "Spooky": ("#17171F", "#20242A"),
    "Nightly": ("#46B2E6", "#BBE0FA"),
    "Love": ("#EF4A73", "#F7A8A0"),
}
# Default style if none provided
selected_style = sys.argv[1] if len(sys.argv) > 1 else "Wood"
style_colors = STYLES.get(selected_style, ("#503E32", "#A26D4C"))

# Get language from command-line arguments
selected_language = sys.argv[4] if len(sys.argv) > 4 else "English"

LANGUAGES = {
    "English": {
        "main_menu": "Main Menu",
        "save_game": "Save Game",
        "load_game": "Load Game",
        "restart_game": "Restart Game",
        "exit": "Exit",
        "turn_label": "Player {}'s TURN",
        "check_alert": "Your king is in check!",
        "checkmate": "Checkmate! {} wins!",
        "invalid_move": "This move is not allowed for the selected piece.",
        "invalid_selection": "You must select a valid piece!",
        "game_saved": "Game has been saved successfully!",
        "game_loaded": "Game has been loaded successfully!",
        "restart_info": "Game has been restarted!",
        "home": "Home",
        "game_rules": "Game Rules",
        "change_view": "Change View",
        "light_mode": "Light Mode",
        "dark_mode": "Dark Mode",
        "white": "White",
        "black": "Black",
        "turn": "Turn",
    },
    "Spanish": {
        "main_menu": "Menú Principal",
        "save_game": "Guardar Partida",
        "load_game": "Cargar Partida",
        "restart_game": "Reiniciar Partida",
        "exit": "Salir",
        "turn_label": "Turno del Jugador {}",
        "check_alert": "¡Tu rey está en jaque!",
        "checkmate": "¡Jaque mate! {} gana!",
        "invalid_move": "Este movimiento no está permitido para la pieza seleccionada.",
        "invalid_selection": "¡Debes seleccionar una pieza válida!",
        "game_saved": "¡La partida se ha guardado con éxito!",
        "game_loaded": "¡La partida se ha cargado con éxito!",
        "restart_info": "¡La partida se ha reiniciado!",
        "home": "Inicio",
        "game_rules": "Reglas del Juego",
        "change_view": "Cambiar Vista",
        "light_mode": "Modo Claro",
        "dark_mode": "Modo Oscuro",
        "white": "Blanco",
        "black": "Negro",
        "turn": "Turno",
    },
    "Turkish": {
        "main_menu": "Ana Menü",
        "save_game": "Oyunu Kaydet",
        "load_game": "Oyunu Yükle",
        "restart_game": "Oyunu Yeniden Başlat",
        "exit": "Çıkış",
        "turn_label": "{} Oyuncusunun Sırası",
        "check_alert": "Şahınız tehdit altında!",
        "checkmate": "Şah mat! {} kazandı!",
        "invalid_move": "Seçilen taş için bu hamle geçersiz.",
        "invalid_selection": "Geçerli bir taş seçmelisiniz!",
        "game_saved": "Oyun başarıyla kaydedildi!",
        "game_loaded": "Oyun başarıyla yüklendi!",
        "restart_info": "Oyun yeniden başlatıldı!",
        "home": "Ana Sayfa",
        "game_rules": "Oyun Kuralları",
        "change_view": "Görünümü Değiştir",
        "light_mode": "Açık Mod",
        "dark_mode": "Koyu Mod",
        "white": "Beyaz",
        "black": "Siyah",
        "turn": "Sıra",
    }
}


current_language = LANGUAGES[selected_language]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Board(tk.Frame):
    def __init__(self, parent, length, width, style_colors):  # Add style_colors parameter
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.length = length
        self.width = width
        self.style_colors = style_colors  # Store the style colors
        self.config(height=100*self.length, width=100*self.width)
        self.pack()

        self.square_color = None
        self.squares = {}
        self.ranks = string.ascii_lowercase
        self.white_images = {}
        self.black_images = {}
        self.set_squares()

        
        self.square_color = None
        self.squares = {} #stores squares with pos as key and button as value
        self.ranks = string.ascii_lowercase
        self.white_images = {} #stores images of pieces
        self.black_images = {}
        self.white_pieces = ["pyimage1", "pyimage3", "pyimage4", "pyimage5", "pyimage6", "pyimage7"] #for convenience when calling all white pieces
        self.black_pieces = ["pyimage8", "pyimage10", "pyimage11", "pyimage12", "pyimage13", "pyimage14"]
        self.buttons_pressed = 0
        self.turns = 0
        self.sq1 = None #first square clicked
        self.sq2 = None 
        self.sq1_button = None #button associated with the square clicked
        self.sq2_button = None
        self.piece_color = None
        self.wk_moved = False #for castling
        self.bk_moved = False
        self.wr1_moved = False
        self.wr2_moved = False
        self.br1_moved = False
        self.br2_moved = False
        self.castled = False
        self.set_squares()
        
    def in_checkmate(self):
        """Check if the current player is in checkmate."""
        for square in self.squares:
            self.sq1 = square
            self.sq1_button = self.squares[square]

            # Skip squares without a piece of the current player's color
            if (self.turns % 2 == 0 and self.sq1_button["image"] not in self.white_pieces) or \
            (self.turns % 2 == 1 and self.sq1_button["image"] not in self.black_pieces):
                continue

            # Test all possible moves for this piece
            for target_square in self.squares:
                self.sq2 = target_square
                self.sq2_button = self.squares[target_square]
                if self.allowed_piece_move() and not self.friendly_fire():
                    # Simulate the move
                    prev_sq1, prev_sq1_image = self.sq1, self.sq1_button["image"]
                    prev_sq2, prev_sq2_image = self.sq2, self.sq2_button["image"]
                    self.squares[self.sq2].config(image=self.squares[self.sq1].cget("image"))
                    self.squares[self.sq1].config(image=self.white_images["blank.png"])

                    # Check if king is still in check
                    if not self.in_check():
                        # Undo the simulated move and return False (not checkmate)
                        self.squares[self.sq1].config(image=prev_sq1_image)
                        self.squares[self.sq2].config(image=prev_sq2_image)
                        return False

                    # Undo the simulated move
                    self.squares[self.sq1].config(image=prev_sq1_image)
                    self.squares[self.sq2].config(image=prev_sq2_image)

        return True
        
    def restart_game(self, move_log_label, turn_label, player1_name):
        """Restart the game by resetting the board and game state."""
        self.set_pieces()
        self.turns = 0
        self.wk_moved = self.bk_moved = False
        self.wr1_moved = self.wr2_moved = False
        self.br1_moved = self.br2_moved = False

        # Clear the move log and update the turn label
        move_log_label.config(text="")
        turn_label.config(text=f"{player1_name}'s TURN")

        messagebox.showinfo("Restart Game", "Game has been restarted!")


    # def select_piece(self, button): #called when a square button is pressed, consists of majority of the movement code
    #     print("Button clicked:", button)
    #     print("Button image:", button["image"])
    #     if self.buttons_pressed == 0:
    #         if button["image"] in self.white_pieces and self.turns % 2 != 0:
    #             messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
    #             return
    #         elif button["image"] in self.black_pieces and self.turns % 2 == 0:
    #             messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
    #             return
    #         elif button["image"] not in self.white_pieces + self.black_pieces:
    #             messagebox.showwarning(current_language["invalid_selection"], current_language["invalid_selection"])
    #             return

    #         # Si la pieza seleccionada es válida, se asigna el color
    #         if button["image"] in self.white_pieces:
    #             self.piece_color = "white"
    #         elif button["image"] in self.black_pieces:
    #             self.piece_color = "black"
        
    #     if (self.piece_color == "white" and self.turns % 2 == 0) or (self.piece_color == "black" and self.turns % 2 == 1) or self.buttons_pressed == 1: #prevents people from moving their pieces when it's not their turn
    #         if self.buttons_pressed == 0: #stores square and button of first square selected
    #             self.sq1 = list(self.squares.keys())[list(self.squares.values()).index(button)] #retrieves pos of piece
    #             self.sq1_button = button
    #             self.buttons_pressed += 1
             
    #         elif self.buttons_pressed==1: #stores square and button of second square selected
    #             self.sq2 = list(self.squares.keys())[list(self.squares.values()).index(button)]
    #             self.sq2_button = button
    #             if self.sq2 == self.sq1: #prevents self-destruction and allows the user to choose a new piece
    #                 self.buttons_pressed = 0
    #                 return
                
    #             if self.allowed_piece_move() and self.friendly_fire() == False:  # Verifica si el movimiento es válido
    #                 prev_sq1 = self.sq1
    #                 prev_sq1_button_piece = self.sq1_button["image"]
    #                 prev_sq2 = self.sq2
    #                 prev_sq2_button_piece = self.sq2_button["image"]

    #                 # Realiza el movimiento
    #                 self.squares[self.sq2].config(image=self.sq1_button["image"])  # Mueve la pieza de sq1 a sq2
    #                 self.squares[self.sq2].image = self.sq1_button["image"]
    #                 self.squares[self.sq1].config(image=self.white_images["blank.png"])  # Limpia la posición anterior
    #                 self.squares[self.sq1].image = self.white_images["blank.png"]

    #                 # Verifica si el rey queda en jaque
    #                 if self.in_check() == True and self.castled == False:  
    #                     # Revertir movimiento porque deja al rey en jaque
    #                     self.squares[prev_sq2].config(image=prev_sq2_button_piece)
    #                     self.squares[prev_sq2].image = prev_sq2_button_piece
    #                     self.squares[prev_sq1].config(image=prev_sq1_button_piece)
    #                     self.squares[prev_sq1].image = prev_sq1_button_piece
    #                     self.buttons_pressed = 0
    #                     # messagebox.showwarning("Invalid Move", "This move puts your king in check!")
    #                     messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
    #                     return

    #                 # Marca las piezas importantes que han sido movidas (para evitar castling)
    #                 if prev_sq1_button_piece == "pyimage3":  # Rey blanco
    #                     self.wk_moved = True
    #                 if prev_sq1_button_piece == "pyimage10":  # Rey negro
    #                     self.bk_moved = True
    #                 if prev_sq1_button_piece == "pyimage7" and prev_sq1 == "a1":  # Torre blanca izquierda
    #                     self.wr1_moved = True
    #                 if prev_sq1_button_piece == "pyimage7" and prev_sq1 == "h1":  # Torre blanca derecha
    #                     self.wr2_moved = True
    #                 if prev_sq1_button_piece == "pyimage14" and prev_sq1 == "a8":  # Torre negra izquierda
    #                     self.br1_moved = True
    #                 if prev_sq1_button_piece == "pyimage14" and prev_sq1 == "h8":  # Torre negra derecha
    #                     self.br2_moved = True

    #                 self.buttons_pressed = 0  # Reinicia la selección

    #                 # Verificar si hay promoción de peón
    #                 if (self.sq1_button["image"] == "pyimage5" and prev_sq2.count("8") == 1) or \
    #                 (self.sq1_button["image"] == "pyimage12" and prev_sq2.count("1") == 1):
    #                     self.promotion_menu(self.piece_color)

    #                 self.castled = False  # Resetear la bandera de enroque

    #                 # Actualizar el registro de movimientos
    #                 move_text = f"{prev_sq1.upper()}->{prev_sq2.upper()}"
    #                 current_log = move_log_label.cget("text").splitlines()

    #                 move_number = (self.turns // 2) + 1  # Número de movimiento
    #                 player = "White" if self.turns % 2 == 0 else "Black"

    #                 if player == "White":
    #                     new_line = f"{move_number}. White: {move_text}"
    #                     current_log.append(new_line)
    #                 else:
    #                     current_log[-1] += f" | Black: {move_text}"

    #                 move_log_label.config(text="\n".join(current_log))
                    
    #                 if self.in_checkmate():
    #                     winner = player1_name if self.turns % 2 != 0 else player2_name
    #                     # messagebox.showinfo("Checkmate", f"Checkmate! {winner} wins!")
    #                     messagebox.showinfo(current_language["checkmate"], current_language["checkmate"].format(player1_name))
    #                     self.restart_game()
    #                     return
                    
    #                 # Incrementar el contador de turnos
    #                 self.turns += 1

    #                 # Actualizar el Turn Label
    #                 if self.turns % 2 == 0:  # Turno par: Player 1
    #                     turn_label.config(text=f"{player1_name}'s TURN")
    #                 else:  # Turno impar: Player 2
    #                     turn_label.config(text=f"{player2_name}'s TURN")
    #             else:
    #                 messagebox.showwarning("Invalid Move", "This move is not allowed for the selected piece.")
                    

    #         else:
    #             self.buttons_pressed = 0
    #             return
    def select_piece(self, button):  # Called when a square button is pressed, consists of majority of the movement code
        print("Button clicked:", button)
        print("Button image:", button["image"])
        
        # First click: Selecting the piece
        if self.buttons_pressed == 0:
            if button["image"] in self.white_pieces and self.turns % 2 != 0:
                messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
                return
            elif button["image"] in self.black_pieces and self.turns % 2 == 0:
                messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
                return
            elif button["image"] not in self.white_pieces + self.black_pieces:
                messagebox.showwarning(current_language["invalid_selection"], current_language["invalid_selection"])
                return

            # If a valid piece is selected, set the color
            if button["image"] in self.white_pieces:
                self.piece_color = "white"
            elif button["image"] in self.black_pieces:
                self.piece_color = "black"

            # Store the first square's position and button
            self.sq1 = list(self.squares.keys())[list(self.squares.values()).index(button)]  # Retrieve position of the piece
            self.sq1_button = button
            self.buttons_pressed += 1

        # Second click: Selecting the destination square
        elif self.buttons_pressed == 1:
            self.sq2 = list(self.squares.keys())[list(self.squares.values()).index(button)]  # Get second square
            self.sq2_button = button

            if self.sq2 == self.sq1:  # Prevent self-destruction and allow the user to choose a new piece
                self.buttons_pressed = 0
                self.sq1 = None
                self.sq2 = None
                return

            if self.allowed_piece_move() and not self.friendly_fire():  # Verify if the move is valid
                prev_sq1 = self.sq1
                prev_sq1_button_piece = self.sq1_button["image"]
                prev_sq2 = self.sq2
                prev_sq2_button_piece = self.sq2_button["image"]

                # Perform the move
                self.squares[self.sq2].config(image=self.sq1_button["image"])  # Move the piece
                self.squares[self.sq2].image = self.sq1_button["image"]
                self.squares[self.sq1].config(image=self.white_images["blank.png"])  # Clear the previous position
                self.squares[self.sq1].image = self.white_images["blank.png"]

                # Verify if the king is in check after the move
                if self.in_check() and not self.castled:
                    # Revert the move if it leaves the king in check
                    self.squares[prev_sq2].config(image=prev_sq2_button_piece)
                    self.squares[prev_sq2].image = prev_sq2_button_piece
                    self.squares[prev_sq1].config(image=prev_sq1_button_piece)
                    self.squares[prev_sq1].image = prev_sq1_button_piece
                    messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])
                    self.buttons_pressed = 0
                    self.sq1 = None
                    self.sq2 = None
                    return

                # Mark important pieces that have moved (to prevent castling)
                if prev_sq1_button_piece == "pyimage3":  # White king
                    self.wk_moved = True
                if prev_sq1_button_piece == "pyimage10":  # Black king
                    self.bk_moved = True
                if prev_sq1_button_piece == "pyimage7" and prev_sq1 == "a1":  # White left rook
                    self.wr1_moved = True
                if prev_sq1_button_piece == "pyimage7" and prev_sq1 == "h1":  # White right rook
                    self.wr2_moved = True
                if prev_sq1_button_piece == "pyimage14" and prev_sq1 == "a8":  # Black left rook
                    self.br1_moved = True
                if prev_sq1_button_piece == "pyimage14" and prev_sq1 == "h8":  # Black right rook
                    self.br2_moved = True

                # Handle pawn promotion
                if (self.sq1_button["image"] == "pyimage5" and prev_sq2.count("8") == 1) or \
                (self.sq1_button["image"] == "pyimage12" and prev_sq2.count("1") == 1):
                    self.promotion_menu(self.piece_color)

                self.castled = False  # Reset castling flag

                # Update the move log
                move_text = f"{prev_sq1.upper()}->{prev_sq2.upper()}"
                current_log = move_log_label.cget("text").splitlines()

                move_number = (self.turns // 2) + 1  # Move number
                white_label = current_language["white"]
                black_label = current_language["black"]

                if self.turns % 2 == 0:  # Player 1 (White)
                    new_line = f"{move_number}. {white_label}: {move_text}"
                    current_log.append(new_line)
                else:  # Player 2 (Black)
                    current_log[-1] += f" | {black_label}: {move_text}"

                move_log_label.config(text="\n".join(current_log))


                # Check if the move caused a checkmate
                if self.in_checkmate():
                    winner = player1_name if self.turns % 2 != 0 else player2_name
                    messagebox.showinfo(current_language["checkmate"], current_language["checkmate"].format(winner))
                    self.restart_game(move_log_label, turn_label, player1_name)
                    return

                # Increment turn counter and update turn label
                self.turns += 1

                if self.turns % 2 == 0:  # Even turn: Player 1
                    turn_label.config(text=current_language["turn_label"].format(player1_name))
                else:  # Odd turn: Player 2
                    turn_label.config(text=current_language["turn_label"].format(player2_name))

            else:
                messagebox.showwarning(current_language["invalid_move"], current_language["invalid_move"])

            # Reset after the second click
            self.buttons_pressed = 0
            self.sq1 = None
            self.sq2 = None

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
            
    def friendly_fire(self): #prevents capturing your own pieces
        piece_2_color = self.sq2_button["image"]
        if self.piece_color == "white" and piece_2_color in self.white_pieces:
            return True
        if self.piece_color == "black" and piece_2_color in self.black_pieces:
            return True
        else:
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
        # Ensure both squares are valid
        if not self.sq1 or not self.sq2:
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
        if not self.sq1 or not self.sq2:
            return False
        return_previous_values()
        return False
    
    def find_king(self, king): #finds the square where the king is currently on
        for square  in self.squares:
            button = self.squares[square]
            if button["image"] == king:
                return square
    
    def set_squares(self): #fills frame with buttons representing squares

        for x in range(8):
            for y in range(8):
                light_color, dark_color = self.style_colors  # Extract style colors
                if x % 2 == 0 and y % 2 == 0 or x % 2 == 1 and y % 2 == 1:
                    self.square_color = dark_color  # Dark squares
                else:
                    self.square_color = light_color  # Light squares


                    
                B = tk.Button(self, bg=self.square_color, activebackground="lawn green")
                B.grid(row=8-x, column=y)
                pos = self.ranks[y]+str(x+1)
                self.squares.setdefault(pos, B) #creates list of square positions
                self.squares[pos].config(command=lambda key=self.squares[pos]: self.select_piece(key))              
        
    def import_pieces(self):  # Opens and stores images of pieces dynamically based on style
        # Dynamically locate the selected style's directories for Black and White pieces
        style_folder = os.path.join(os.path.dirname(__file__), "assets", "Styles", selected_style)
        path_white = os.path.join(style_folder, "White")
        path_black = os.path.join(style_folder, "Black")

        # Verify if the paths exist
        if not os.path.exists(path_white):
            print(f"Error: White pieces directory not found -> {path_white}")
            return
        if not os.path.exists(path_black):
            print(f"Error: Black pieces directory not found -> {path_black}")
            return

        # Load white piece images
        white_files = os.listdir(path_white)
        for file in white_files:
            img_path = os.path.join(path_white, file)
            if os.path.isfile(img_path):
                img = Image.open(img_path).resize((80, 80), Image.LANCZOS)
                img = ImageTk.PhotoImage(image=img)
                self.white_images[file] = img  # Store images with filenames as keys
            else:
                print(f"Warning: File not found -> {img_path}")

        # Load black piece images
        black_files = os.listdir(path_black)
        for file in black_files:
            img_path = os.path.join(path_black, file)
            if os.path.isfile(img_path):
                img = Image.open(img_path).resize((80, 80), Image.LANCZOS)
                img = ImageTk.PhotoImage(image=img)
                self.black_images[file] = img  # Store images with filenames as keys
            else:
                print(f"Warning: File not found -> {img_path}")



    def set_pieces(self): #places pieces in starting positions
        dict_rank1_pieces = {"a1":"r.png", "b1":"n.png", "c1":"b.png", "d1":"q.png", "e1":"k.png", "f1":"b.png", "g1":"n.png", "h1":"r.png"} #assigning positions with their default pieces
        dict_rank2_pieces = {"a2":"p.png", "b2":"p.png", "c2":"p.png", "d2":"p.png", "e2":"p.png", "f2":"p.png", "g2":"p.png", "h2":"p.png"}     
        dict_rank7_pieces = {"a7":"p.png", "b7":"p.png", "c7":"p.png", "d7":"p.png", "e7":"p.png", "f7":"p.png", "g7":"p.png", "h7":"p.png"}
        dict_rank8_pieces = {"a8":"r.png", "b8":"n.png", "c8":"b.png", "d8":"q.png", "e8":"k.png", "f8":"b.png", "g8":"n.png", "h8":"r.png"}

        for key in dict_rank1_pieces: #inserts images into buttons
            starting_piece = dict_rank1_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image = self.white_images[starting_piece]
            
        for key in dict_rank2_pieces:
            starting_piece = dict_rank2_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image = self.white_images[starting_piece]
            
        for key in dict_rank7_pieces:
            starting_piece = dict_rank7_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image = self.black_images[starting_piece]
            
        for key in dict_rank8_pieces:
            starting_piece = dict_rank8_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image = self.black_images[starting_piece]

        for rank in range(3,7): #fill rest with blank pieces
            for file in range(8):
                starting_piece = "blank.png"
                pos = self.ranks[file]+str(rank)
                self.squares[pos].config(image=self.white_images[starting_piece])
                self.squares[pos].image = self.white_images[starting_piece]


# Functionality for the menu options
def home_action():
    root.destroy()
    os.startfile(os.path.join(os.path.dirname(__file__), "MainMenu.pyw"))

def save_game_action(board, move_log_label, turn_label, player1_name):
    """Save the current game state to a .pkl file and automatically restart the game."""
    try:
        # Ask the user for the save file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            title="Save Game"
        )
        if not file_path:  # If the user cancels
            return

        # Create a dictionary with the game's state
        game_state = {
            "turns": board.turns,
            "board": {pos: button["image"] for pos, button in board.squares.items()},
            "wk_moved": board.wk_moved,
            "bk_moved": board.bk_moved,
            "wr1_moved": board.wr1_moved,
            "wr2_moved": board.wr2_moved,
            "br1_moved": board.br1_moved,
            "br2_moved": board.br2_moved,
            "move_log": move_log_label.cget("text"),  # Save move log text
            "turn_label": turn_label.cget("text"),  # Save turn label text
        }

        # Save the game state using pickle
        with open(file_path, "wb") as save_file:
            pickle.dump(game_state, save_file)

        messagebox.showinfo("Save Game", "Game has been saved successfully!")

        # Automatically restart the game after saving
        board.restart_game(move_log_label, turn_label, player1_name)


    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving: {str(e)}")

def load_game_action(board, move_log_label, turn_label):
    """Load a previously saved game from a .pkl file."""
    try:
        file_path = filedialog.askopenfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            title="Load Game"
        )
        if not file_path:  # If user cancels
            return

        # Load the game state using pickle
        with open(file_path, "rb") as load_file:
            game_state = pickle.load(load_file)

        # Restore the game's state
        board.turns = game_state["turns"]
        board.wk_moved = game_state["wk_moved"]
        board.bk_moved = game_state["bk_moved"]
        board.wr1_moved = game_state["wr1_moved"]
        board.wr2_moved = game_state["wr2_moved"]
        board.br1_moved = game_state["br1_moved"]
        board.br2_moved = game_state["br2_moved"]

        # Restore the board
        for pos, image_name in game_state["board"].items():
            board.squares[pos].config(image=image_name)
            board.squares[pos].image = image_name

        # Restore the move log
        move_log_label.config(text=game_state["move_log"])

        # Restore the turn label
        turn_label.config(text=game_state["turn_label"])

        messagebox.showinfo("Load Game", "Game has been loaded successfully!")

    except Exception as e:
        messagebox.showerror("Load Error", f"An error occurred while loading: {str(e)}")


def restart_game(self, move_log_label, turn_label, player1_name):
    """Restart the game by resetting the board and game state."""
    self.set_pieces()
    self.turns = 0
    self.wk_moved = self.bk_moved = False
    self.wr1_moved = self.wr2_moved = False
    self.br1_moved = self.br2_moved = False

    # Clear the move log and update the turn label
    move_log_label.config(text="")
    turn_label.config(text=current_language["turn_label"].format(player1_name))

    messagebox.showinfo(current_language["restart_game"], current_language["restart_info"])


def game_rules_action():
    # Show game rules in a message box
    os.startfile(os.path.join(os.path.dirname(__file__), "Game_Rules.pyw"))
    
def change_view(mode):
    """Switch between Light Mode and Dark Mode."""
    if mode == "Light Mode":
        # Set backgrounds for Light Mode
        root.config(bg="white")
        board.config(bg="white")
        right_frame.config(bg="white")
        ui_frame.config(bg="white")
        
        # Turn label: Adapts text color based on window background
        turn_label.config(bg="white", fg="black")
        
        # Move log label
        move_log_label.config(bg="white", fg="black")
        
        # Menu button
        menu_button.config(bg="white", fg="black", relief="flat", bd=0)
        turn_label.config(bg="white", fg="black", highlightbackground="black", highlightthickness=2)
        move_log_label.config(bg="white", fg="black", highlightbackground="black", highlightthickness=2)
        
    elif mode == "Dark Mode":
        # Set backgrounds for Dark Mode
        root.config(bg="black")
        board.config(bg="black")
        right_frame.config(bg="black")
        ui_frame.config(bg="black")
        
        # Turn label: Adapts text color based on window background
        turn_label.config(bg="black", fg="white")
        
        # Move log label
        move_log_label.config(bg="black", fg="white")
        
        # Menu button
        menu_button.config(bg="black", fg="white", relief="flat", bd=0)
        turn_label.config(bg="black", fg="white", highlightbackground="white", highlightthickness=2)
        move_log_label.config(bg="black", fg="white", highlightbackground="white", highlightthickness=2)


def exit_action():
    root.quit()

# Create the Tkinter root window
root = tk.Tk()
root.geometry("800x800")
root.state("zoomed")
root.title("Chess Game")
root.configure(background="white")
icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")
root.iconbitmap(icon_path)
# Create the menu bar
menu_bar = tk.Menu(root)

# Add the "Home" menu
home_menu = tk.Menu(menu_bar, tearoff=0)
home_menu.add_command(label=current_language["home"], command=home_action)
menu_bar.add_cascade(label=current_language["home"], menu=home_menu)

# Add the "Main Menu" menu with suboptions
main_menu = tk.Menu(menu_bar, tearoff=0)
# main_menu.add_command(
#     label="Save Game", 
#     command=lambda: save_game_action(board, move_log_label, turn_label, player1_name)
# )
# main_menu.add_command(label="Load Game", command=lambda: load_game_action(board, move_log_label, turn_label))
# main_menu.add_command(
#     label="Restart Game", 
#     command=lambda: board.restart_game(move_log_label, turn_label, player1_name)
# )

# Main Menu
main_menu.add_command(label=current_language["save_game"], command=lambda: save_game_action(board, move_log_label, turn_label, player1_name))
main_menu.add_command(label=current_language["load_game"], command=lambda: load_game_action(board, move_log_label, turn_label))
main_menu.add_command(label=current_language["restart_game"], command=lambda: board.restart_game(move_log_label, turn_label, player1_name))

menu_bar.add_cascade(label=current_language["main_menu"], menu=main_menu)

# Add the "Game Rules" menu
rules_menu = tk.Menu(menu_bar, tearoff=0)
rules_menu.add_command(label=current_language["game_rules"], command=game_rules_action)
menu_bar.add_cascade(label=current_language["game_rules"], menu=rules_menu)

# Add the "Change View" menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label=current_language["light_mode"], command=lambda: change_view("Light Mode"))
view_menu.add_command(label=current_language["dark_mode"], command=lambda: change_view("Dark Mode"))
menu_bar.add_cascade(label=current_language["change_view"], menu=view_menu)

# Left-side UI Frame for Menu Button
ui_frame = tk.Frame(root, bg="white", width=100)
ui_frame.pack(fill="y", side="left")

# Right-side Frame for Turn Label and Move Log
right_frame = tk.Frame(root, bg="white", width=200)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

# Menu Button
menu_button = tk.Button(ui_frame, text="Menu", font=("Arial", 14, "bold"),
                        command=lambda: messagebox.showinfo("Menu", "Chess Game Menu"))
menu_button.pack(pady=20)

# Turn Label with Black Border
turn_label = tk.Label(
    right_frame,
    text=LANGUAGES[selected_language]["turn_label"].format(player1_name),
    font=("Arial", 18, "bold"),
    bg="white",
    fg="black",
    highlightbackground="black",  # Border color
    highlightthickness=2,         # Border thickness
    highlightcolor="black"        # Highlight color (active border)
)
turn_label.pack(pady=(10, 20), fill="x")

# Move Log Label with Black Border
move_log_label = tk.Label(
    right_frame,
    text="",
    font=("Arial", 14),
    anchor="nw",
    justify="left",
    bg="white",
    fg="black",
    highlightbackground="black",  # Border color
    highlightthickness=2,         # Border thickness
    highlightcolor="black"        # Highlight color (active border)
)
move_log_label.pack(fill="both", expand=True)

# Add the "Exit" menu
exit_menu = tk.Menu(menu_bar, tearoff=0)
exit_menu.add_command(label=current_language["exit"], command=exit_action)
menu_bar.add_cascade(label=current_language["exit"], menu=exit_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Chess Board Initialization
board = Board(root, 8, 8, style_colors)
board.import_pieces()
board.set_pieces()


# Start the main loop
root.mainloop()
