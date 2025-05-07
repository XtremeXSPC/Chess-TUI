# pieces.py
"""Definisce le classi per i pezzi degli scacchi."""

from abc import ABC, abstractmethod
from typing import List, Tuple, TYPE_CHECKING

from .constants import Color, PIECE_SYMBOLS, IDX_TO_COL

if TYPE_CHECKING:
    from .board import Board  # Evita import circolare in fase di runtime


class Piece(ABC):
    """Classe base astratta per tutti i pezzi degli scacchi."""

    def __init__(self, color: Color, position: Tuple[int, int]):
        """
        Inizializza un pezzo.

        Args:
            color: Il colore del pezzo (WHITE o BLACK).
            position: La posizione (riga, colonna) sulla scacchiera (0-7).
        """
        if not isinstance(color, Color):
            raise TypeError("Il colore deve essere un'istanza di Color Enum")
        self._color = color
        self._position = position
        self._has_moved = False  # Utile per arrocco, movimento iniziale pedone

    @property
    def color(self) -> Color:
        """Restituisce il colore del pezzo."""
        return self._color

    @property
    def position(self) -> Tuple[int, int]:
        """Restituisce la posizione (riga, colonna) del pezzo."""
        return self._position

    @position.setter
    def position(self, new_position: Tuple[int, int]):
        """
        Imposta la nuova posizione del pezzo.

        Args:
            new_position: La nuova posizione (riga, colonna).
        """
        # Qui si potrebbe aggiungere validazione se la posizione è sulla scacchiera,
        # ma è generalmente gestita da Board.is_within_bounds prima di chiamare questo.
        self._position = new_position
        self._has_moved = True  # Il pezzo si è mosso

    @property
    def has_moved(self) -> bool:
        """Indica se il pezzo si è già mosso."""
        return self._has_moved

    @abstractmethod
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        """
        Restituisce una lista di mosse valide per questo pezzo sulla scacchiera data.
        Questo metodo deve essere implementato dalle sottoclassi.
        Per lo Sprint 1, per i pedoni, restituisce solo mosse di avanzamento.

        Args:
            board: L'oggetto scacchiera corrente.

        Returns:
            Lista di posizioni (riga, colonna) valide per la mossa.
        """
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """Restituisce il simbolo Unicode o la lettera per questo pezzo."""
        pass

    def __str__(self) -> str:
        """Rappresentazione stringa del pezzo (utile per il debug)."""
        row_idx, col_idx = self.position
        # Assicura che IDX_TO_COL esista e che col_idx sia una chiave valida
        col_char = IDX_TO_COL.get(col_idx, '?') # '?' se col_idx non fosse valido
        return f"{self.get_symbol()} ({self.color.name}) at {col_char}{row_idx + 1}"

    def __repr__(self) -> str:
        """Rappresentazione ufficiale del pezzo."""
        return f"{self.__class__.__name__}(color={self.color}, position={self.position})"


class Pawn(Piece):
    """Rappresenta un pedone."""

    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]

    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        """
        Calcola le mosse valide per un pedone.
        Per lo Sprint 1:
        - Movimento in avanti di una casa.
        - Movimento iniziale in avanti di due case.
        - NON include catture (né normali né en passant).

        Args:
            board: L'oggetto scacchiera corrente.

        Returns:
            Lista di posizioni (riga, colonna) di destinazione valide per l'avanzamento.
        """
        valid_moves = []
        row, col = self.position
        direction = 1 if self.color == Color.WHITE else -1  # Bianco va verso righe > , Nero verso righe <

        # 1. Mossa in avanti di una casa
        one_step_forward = (row + direction, col)
        if board.is_within_bounds(one_step_forward) and board.get_piece(one_step_forward) is None:
            valid_moves.append(one_step_forward)

            # 2. Mossa iniziale in avanti di due case (solo se la prima casa è libera)
            if not self.has_moved: # Può muovere di due solo se non si è mai mosso
                two_steps_forward = (row + 2 * direction, col)
                # Deve essere nei limiti e la casa di destinazione deve essere vuota
                if board.is_within_bounds(two_steps_forward) and board.get_piece(two_steps_forward) is None:
                    valid_moves.append(two_steps_forward)

        # 3. Catture (NON implementate nello Sprint 1)
        #    Le mosse di cattura (diagonali) verrebbero aggiunte qui in sprint futuri.
        #    Esempio:
        #    for d_col in [-1, 1]:
        #        capture_pos = (row + direction, col + d_col)
        #        if board.is_within_bounds(capture_pos):
        #            target_piece = board.get_piece(capture_pos)
        #            if target_piece and target_piece.color != self.color:
        #                valid_moves.append(capture_pos)
        # TODO: Implementare cattura en passant

        return valid_moves


class Rook(Piece):
    """Rappresenta una Torre."""
    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        # TODO: Implementare logica movimento Torre
        return []

class Knight(Piece):
    """Rappresenta un Cavallo."""
    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        # TODO: Implementare logica movimento Cavallo
        return []

class Bishop(Piece):
    """Rappresenta un Alfiere."""
    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        # TODO: Implementare logica movimento Alfiere
        return []

class Queen(Piece):
    """Rappresenta una Regina."""
    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        # TODO: Implementare logica movimento Regina
        return []

class King(Piece):
    """Rappresenta un Re."""
    def get_symbol(self) -> str:
        return PIECE_SYMBOLS[(self.color, self.__class__.__name__)]
    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        # TODO: Implementare logica movimento Re (incl. non muovere in scacco)
        return []