# board.py
"""Definisce la classe Board per rappresentare la scacchiera."""

from typing import List, Tuple, Optional, Dict

# Assumiamo che 'constants.py' e 'pieces.py' siano nello stesso pacchetto o PYTHONPATH
from .constants import Color, BOARD_SIZE, IDX_TO_COL, COL_TO_IDX
from .pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King # Importa tutte le classi pezzo


class Board:
    """Rappresenta la scacchiera e gestisce i pezzi."""

    def __init__(self):
        """Inizializza una scacchiera vuota."""
        # Usiamo un dizionario per memorizzare i pezzi: chiave = (riga, colonna), valore = Oggetto Piece
        # Questo è efficiente per cercare un pezzo in una data posizione.
        self._grid: Dict[Tuple[int, int], Piece] = {}
        self.setup_pieces() # Imposta i pezzi nella posizione iniziale

    def setup_pieces(self):
        """Dispone i pezzi sulla scacchiera nella configurazione iniziale."""
        self._grid = {} # Pulisce la scacchiera prima di aggiungere i pezzi

        # Pedoni
        for col in range(BOARD_SIZE):
            self._grid[(1, col)] = Pawn(Color.WHITE, (1, col))
            self._grid[(6, col)] = Pawn(Color.BLACK, (6, col))

        # Pezzi principali Bianchi (riga 0)
        self._grid[(0, 0)] = Rook(Color.WHITE, (0, 0))
        self._grid[(0, 7)] = Rook(Color.WHITE, (0, 7))
        self._grid[(0, 1)] = Knight(Color.WHITE, (0, 1))
        self._grid[(0, 6)] = Knight(Color.WHITE, (0, 6))
        self._grid[(0, 2)] = Bishop(Color.WHITE, (0, 2))
        self._grid[(0, 5)] = Bishop(Color.WHITE, (0, 5))
        self._grid[(0, 3)] = Queen(Color.WHITE, (0, 3))
        self._grid[(0, 4)] = King(Color.WHITE, (0, 4))

        # Pezzi principali Neri (riga 7)
        self._grid[(7, 0)] = Rook(Color.BLACK, (7, 0))
        self._grid[(7, 7)] = Rook(Color.BLACK, (7, 7))
        self._grid[(7, 1)] = Knight(Color.BLACK, (7, 1))
        self._grid[(7, 6)] = Knight(Color.BLACK, (7, 6))
        self._grid[(7, 2)] = Bishop(Color.BLACK, (7, 2))
        self._grid[(7, 5)] = Bishop(Color.BLACK, (7, 5))
        self._grid[(7, 3)] = Queen(Color.BLACK, (7, 3))
        self._grid[(7, 4)] = King(Color.BLACK, (7, 4))

    def get_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        """
        Restituisce il pezzo alla posizione specificata.

        Args:
            position (Tuple[int, int]): La posizione (riga, colonna) da controllare.

        Returns:
            Optional[Piece]: L'oggetto Piece se presente, altrimenti None.
        """
        return self._grid.get(position)

    def move_piece(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Optional[Piece]:
        """
        Muove un pezzo dalla posizione di partenza a quella di arrivo.
        Gestisce la rimozione del pezzo dalla casa di partenza e l'aggiornamento
        della posizione del pezzo. Se la casa di arrivo è occupata,
        il pezzo catturato viene restituito.

        Args:
            start_pos (Tuple[int, int]): Posizione di partenza (riga, colonna).
            end_pos (Tuple[int, int]): Posizione di arrivo (riga, colonna).

        Returns:
            Optional[Piece]: Il pezzo catturato, se presente, altrimenti None.

        Raises:
            ValueError: Se non c'è un pezzo alla posizione di partenza.
        """
        piece_to_move = self.get_piece(start_pos)
        if piece_to_move is None:
            raise ValueError(f"Nessun pezzo trovato alla posizione di partenza {start_pos}")

        captured_piece = self.get_piece(end_pos) # Controlla se c'è un pezzo da catturare

        # Rimuove il pezzo dalla vecchia posizione
        del self._grid[start_pos]

        # Aggiorna la posizione del pezzo e mettilo nella nuova posizione sulla griglia
        piece_to_move.position = end_pos
        self._grid[end_pos] = piece_to_move

        return captured_piece # Restituisce il pezzo catturato (o None)

    def is_within_bounds(self, position: Tuple[int, int]) -> bool:
        """
        Controlla se una posizione è all'interno dei limiti della scacchiera.

        Args:
            position (Tuple[int, int]): La posizione (riga, colonna) da controllare.

        Returns:
            bool: True se la posizione è valida, False altrimenti.
        """
        row, col = position
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_all_pieces(self) -> List[Piece]:
        """Restituisce una lista di tutti i pezzi attualmente sulla scacchiera."""
        return list(self._grid.values())

    def get_pieces_by_color(self, color: Color) -> List[Piece]:
        """Restituisce una lista di tutti i pezzi di un dato colore."""
        return [piece for piece in self._grid.values() if piece.color == color]

    def __str__(self) -> str:
        """Restituisce una rappresentazione testuale semplice della scacchiera (per debug)."""
        board_str = ""
        for r in range(BOARD_SIZE - 1, -1, -1): # Stampa dalla riga 8 alla 1
            row_str = f"{r + 1} "
            for c in range(BOARD_SIZE):
                piece = self.get_piece((r, c))
                row_str += f" {piece.get_symbol() if piece else '.'} "
            board_str += row_str + "\n"
        # Aggiunge le lettere delle colonne in basso
        board_str += "   " + "  ".join([IDX_TO_COL[c] for c in range(BOARD_SIZE)]) + "\n"
        return board_str

