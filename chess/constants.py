# constants.py
"""Definisce le costanti usate nel gioco degli scacchi."""

from enum import Enum

class Color(Enum):
    """Enum per rappresentare i colori dei giocatori (Bianco e Nero)."""
    WHITE = "white"
    BLACK = "black"

# Simboli Unicode per i pezzi (iniziamo con i pedoni)
# Potremmo usare lettere (P, N, B, R, Q, K) se Unicode non è supportato ovunque
PIECE_SYMBOLS = {
    (Color.WHITE, 'Pawn'): "♙",
    (Color.BLACK, 'Pawn'): "♟",
    # Aggiungere altri pezzi qui...
    (Color.WHITE, 'Rook'): "♖",
    (Color.BLACK, 'Rook'): "♜",
    (Color.WHITE, 'Knight'): "♘",
    (Color.BLACK, 'Knight'): "♞",
    (Color.WHITE, 'Bishop'): "♗",
    (Color.BLACK, 'Bishop'): "♝",
    (Color.WHITE, 'Queen'): "♕",
    (Color.BLACK, 'Queen'): "♛",
    (Color.WHITE, 'King'): "♔",
    (Color.BLACK, 'King'): "♚",
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
