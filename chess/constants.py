# constants.py
"""Definisce le costanti usate nel gioco degli scacchi."""

from enum import Enum

class Color(Enum):
    """Enum per rappresentare i colori dei giocatori (Bianco e Nero)."""
    WHITE = "white"
    BLACK = "black"

# Simboli Unicode per i pezzi
PIECE_SYMBOLS = {
    (Color.WHITE, 'Pawn'): "♙", (Color.BLACK, 'Pawn'): "♟",
    (Color.WHITE, 'Rook'): "♖", (Color.BLACK, 'Rook'): "♜",
    (Color.WHITE, 'Knight'): "♘", (Color.BLACK, 'Knight'): "♞",
    (Color.WHITE, 'Bishop'): "♗", (Color.BLACK, 'Bishop'): "♝",
    (Color.WHITE, 'Queen'): "♕", (Color.BLACK, 'Queen'): "♛",
    (Color.WHITE, 'King'): "♔", (Color.BLACK, 'King'): "♚",
}

# Mappatura colonne notazione algebrica -> indice numerico (0-7)
COL_TO_IDX = {chr(ord('a') + i): i for i in range(8)}
# Mappatura indice numerico -> colonne notazione algebrica
IDX_TO_COL = {v: k for k, v in COL_TO_IDX.items()}

# Dimensioni della scacchiera
BOARD_SIZE = 8

# Comandi disponibili
COMMANDS = {
    "/help": "Mostra questo messaggio di aiuto.",
    "/gioca": "Inizia una nuova partita.",
    "/scacchiera": "Mostra la scacchiera attuale.",
    "/abbandona": "Abbandona la partita corrente.",
    "/patta": "Proponi una patta all'avversario.",
    "/mosse": "Mostra l'elenco delle mosse giocate.",
    "/esci": "Esci dal gioco.",
}

# Usato da UI.set_accent_color per validare i colori
RICH_COLORS: set[str] = {
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
    "grey50", # Esempio di altro colore supportato da Rich
    # Aggiungere altri colori di Rich se necessario
}