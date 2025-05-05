# utils.py
"""Fornisce funzioni di utilità per il gioco degli scacchi."""

from typing import Tuple, Optional, List

# Assumiamo che 'constants.py' sia nello stesso pacchetto o PYTHONPATH
from .constants import COL_TO_IDX, IDX_TO_COL, BOARD_SIZE, Color
# Assumiamo che 'pieces.py' e 'board.py' siano nello stesso pacchetto o PYTHONPATH
from .pieces import Piece, Pawn # Importa Pawn specificamente se serve per la notazione
from .board import Board


def algebraic_to_coords(algebraic_notation: str) -> Optional[Tuple[int, int]]:
    """
    Converte la notazione algebrica (es. "e4") in coordinate (riga, colonna).
    Le righe vanno da 0 a 7 (corrispondenti a 1-8), le colonne da 0 a 7 (a-h).

    Args:
        algebraic_notation (str): La notazione algebrica (es. "a1", "h8").

    Returns:
        Optional[Tuple[int, int]]: Coordinate (riga, colonna) o None se la notazione non è valida.
    """
    algebraic_notation = algebraic_notation.lower().strip()
    if len(algebraic_notation) != 2:
        return None # La notazione deve avere 2 caratteri (es. 'e4')

    col_char = algebraic_notation[0]
    row_char = algebraic_notation[1]

    if col_char not in COL_TO_IDX or not row_char.isdigit():
        return None # Colonna o riga non valida

    col = COL_TO_IDX[col_char]
    row = int(row_char) - 1 # Converti '1'-'8' in 0-7

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None # Coordinate fuori dalla scacchiera

    return (row, col)

def coords_to_algebraic(coords: Tuple[int, int]) -> Optional[str]:
    """
    Converte coordinate (riga, colonna) in notazione algebrica.

    Args:
        coords (Tuple[int, int]): Coordinate (riga, colonna) (0-7).

    Returns:
        Optional[str]: Notazione algebrica (es. "e4") o None se le coordinate non sono valide.
    """
    row, col = coords
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None

    col_char = IDX_TO_COL[col]
    row_char = str(row + 1) # Converti 0-7 in '1'-'8'

    return col_char + row_char

def parse_move(move_string: str, board: Board, current_player: Color) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Interpreta una mossa inserita dall'utente in notazione algebrica abbreviata
    e la traduce in coordinate di partenza e arrivo.
    Per lo Sprint 1, gestisce solo mosse di pedone semplici (es. "e4").
    NON gestisce: catture ("exd5"), pezzi diversi dai pedoni ("Cf3"),
                 disambiguazioni ("Rae1"), arrocco ("O-O"), promozione ("e8=Q").

    Args:
        move_string (str): La mossa inserita dall'utente (es. "e4").
        board (Board): L'oggetto scacchiera corrente.
        current_player (Color): Il colore del giocatore che deve muovere.

    Returns:
        Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
            Una tupla contenente (start_coords, end_coords) se la mossa è
            interpretabile e valida per un pedone, altrimenti None.
            Restituisce None anche se la mossa non è sintatticamente valida
            o se più pezzi possono fare quella mossa (richiede disambiguazione).
    """
    move_string = move_string.strip()

    # 1. Prova a interpretare come destinazione diretta (es. "e4")
    end_coords = algebraic_to_coords(move_string)
    if end_coords:
        # Cerca un pedone del colore corrente che possa muovere a end_coords
        possible_starts: List[Tuple[int, int]] = []
        player_pawns = [p for p in board.get_pieces_by_color(current_player) if isinstance(p, Pawn)]

        for pawn in player_pawns:
            valid_moves = pawn.get_valid_moves(board) # Ottiene le mosse valide *senza cattura*
            if end_coords in valid_moves:
                possible_starts.append(pawn.position)

        if len(possible_starts) == 1:
            # Trovato esattamente un pedone che può fare questa mossa
            start_coords = possible_starts[0]
            return (start_coords, end_coords)
        elif len(possible_starts) > 1:
            # Ambiguità: più pedoni possono andare lì (raro senza catture, ma possibile)
            print(f"Ambiguità: più pedoni possono muovere a {move_string}.") # Messaggio all'utente
            return None
        else:
            # Nessun pedone può fare questa mossa (o la mossa non è valida per un pedone)
            # Potrebbe essere una mossa di un altro pezzo (non gestito in Sprint 1)
            # o una mossa non valida.
            # print(f"Nessun pedone può muovere a {move_string} o mossa non valida.")
            return None # Indica che non è una mossa di pedone valida/interpretabile

    # 2. TODO: Gestire altri formati di notazione (es. "Pe4", "Cf3", "exd5", etc.)
    # Per lo Sprint 1, ci fermiamo qui.

    return None # Se non corrisponde a "e4" ecc.

