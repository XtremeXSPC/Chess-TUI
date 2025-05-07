# utils.py
"""Fornisce funzioni di utilità per il gioco degli scacchi."""

from typing import Tuple, Optional, List

from .constants import COL_TO_IDX, IDX_TO_COL, BOARD_SIZE, Color
from .pieces import Piece, Pawn
from .board import Board


def algebraic_to_coords(algebraic_notation: str) -> Optional[Tuple[int, int]]:
    """
    Converte la notazione algebrica (es. "e4") in coordinate (riga, colonna).
    Le righe vanno da 0 a 7 (corrispondenti a 1-8), le colonne da 0 a 7 (a-h).

    Args:
        algebraic_notation: La notazione algebrica (es. "a1", "h8").

    Returns:
        Coordinate (riga, colonna) o None se la notazione non è valida.
    """
    algebraic_notation = algebraic_notation.lower().strip()
    if len(algebraic_notation) != 2:
        return None  # La notazione deve avere 2 caratteri (es. 'e4')

    col_char = algebraic_notation[0]
    row_char = algebraic_notation[1]

    if col_char not in COL_TO_IDX or not row_char.isdigit():
        return None  # Colonna o riga non valida

    col = COL_TO_IDX[col_char]
    row = int(row_char) - 1  # Converti '1'-'8' in 0-7

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None  # Coordinate fuori dalla scacchiera

    return (row, col)

def coords_to_algebraic(coords: Tuple[int, int]) -> Optional[str]:
    """
    Converte coordinate (riga, colonna) in notazione algebrica.

    Args:
        coords: Coordinate (riga, colonna) (0-7).

    Returns:
        Notazione algebrica (es. "e4") o None se le coordinate non sono valide.
    """
    row, col = coords
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None

    # Assicurarsi che col sia una chiave valida per IDX_TO_COL
    col_char = IDX_TO_COL.get(col)
    if col_char is None: # Dovrebbe essere impossibile se col è in range 0-7
        return None
        
    row_char = str(row + 1)  # Converti 0-7 in '1'-'8'

    return col_char + row_char

def parse_move(move_string: str, board: Board, current_player: Color) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Interpreta una mossa inserita dall'utente in notazione algebrica abbreviata
    (es. "e4") e la traduce in coordinate di partenza e arrivo.
    Per lo Sprint 1, gestisce solo mosse di pedone semplici.

    Args:
        move_string: La mossa inserita dall'utente (es. "e4").
        board: L'oggetto scacchiera corrente.
        current_player: Il colore del giocatore che deve muovere.

    Returns:
        Una tupla contenente (start_coords, end_coords) se la mossa è
        interpretabile e valida per un pedone, altrimenti None.
    """
    move_string = move_string.strip().lower()

    # 1. Prova a interpretare come destinazione diretta (es. "e4")
    end_coords = algebraic_to_coords(move_string)
    if end_coords:
        # Cerca un pedone del colore corrente che possa muovere a end_coords
        possible_starts: List[Tuple[int, int]] = []
        player_pawns = [p for p in board.get_pieces_by_color(current_player) if isinstance(p, Pawn)]

        for pawn in player_pawns:
            # get_valid_moves per Pawn (Sprint 1) restituisce solo mosse di avanzamento.
            # Non include catture.
            valid_pawn_advances = pawn.get_valid_moves(board)
            if end_coords in valid_pawn_advances:
                # Verifica addizionale che la casa di destinazione sia vuota
                # (get_valid_moves di Pawn già lo fa, ma è una doppia sicurezza)
                if board.get_piece(end_coords) is None:
                    possible_starts.append(pawn.position)

        if len(possible_starts) == 1:
            start_coords = possible_starts[0]
            return (start_coords, end_coords)
        elif len(possible_starts) > 1:
            # Ambiguità: più pedoni possono andare lì.
            # Per lo Sprint 1 (solo avanzamento pedoni), è raro ma possibile.
            # L'utente dovrà usare la notazione completa tipo "e2e4".
            # Non stampiamo messaggi qui, Game lo gestirà.
            return None # Indica ambiguità o mossa non trovata con questo parser
        else:
            # Nessun pedone può fare questa mossa di avanzamento.
            return None

    # 2. TODO: Gestire altri formati di notazione (es. "Cf3", "exd5", etc.)
    #    e pezzi diversi dai pedoni. Per lo Sprint 1, questo è sufficiente.

    return None # Se non corrisponde a una mossa di pedone abbreviata valida