import os
import sys
import pytest

# Add the project root directory to the Python path
# Assumendo che test_main.py sia in una sottocartella 'tests'
# e la cartella 'scacchi' sia allo stesso livello di 'tests'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chess.ui import UI
from chess.constants import RICH_COLORS # Import per testare i colori validi

# Test per la classe UI
class TestUI:

    def test_ui_default_accent_color(self):
        """Testa che il colore di accento predefinito sia 'blue'."""
        ui = UI()
        assert ui.get_accent_color() == "blue"

    def test_ui_set_valid_accent_color(self):
        """Testa l'impostazione di un colore di accento valido."""
        ui = UI()
        ui.set_accent_color("green")
        assert ui.get_accent_color() == "green"

        ui.set_accent_color("bright_yellow")
        assert ui.get_accent_color() == "bright_yellow"

    def test_ui_set_invalid_accent_color_maintains_previous(self, capsys):
        """
        Testa che impostando un colore di accento non valido,
        il colore precedente venga mantenuto e venga stampato un messaggio.
        """
        ui = UI()
        initial_color = ui.get_accent_color() # Dovrebbe essere "blue"
        
        invalid_color = "fuscia_impossibile"
        ui.set_accent_color(invalid_color)
        
        # Il colore di accento dovrebbe rimanere quello iniziale
        assert ui.get_accent_color() == initial_color, \
            "Il colore di accento è cambiato nonostante l'input non valido."

        # Verifica che sia stato stampato un messaggio di errore
        captured = capsys.readouterr()
        assert "Errore:" in captured.out
        assert f"Colore '{invalid_color}' non valido" in captured.out
        assert f"rimane '{initial_color}'" in captured.out


    def test_ui_get_accent_color_consistency(self):
        """Testa che get_accent_color restituisca consistentemente il colore impostato."""
        ui = UI()
        assert ui.get_accent_color() == "blue" # Default

        ui.set_accent_color("cyan")
        assert ui.get_accent_color() == "cyan"

        ui.set_accent_color("red")
        assert ui.get_accent_color() == "red"

    def test_rich_colors_constant_exists_and_is_set(self):
        """Verifica che la costante RICH_COLORS esista e sia un set."""
        assert isinstance(RICH_COLORS, set)
        assert len(RICH_COLORS) > 0 # Assicura che non sia vuoto
        assert "blue" in RICH_COLORS # Un colore base deve esserci

# Potresti aggiungere altri test per altre parti del sistema qui,
# ad esempio per `Board`, `Game` (con mock UI), `utils`, etc.
# Esempio (molto basilare) per Board:
from chess.board import Board
from chess.constants import Color
from chess.pieces import Pawn

class TestBoard:
    def test_board_setup(self):
        board = Board()
        # Verifica qualche pezzo chiave
        assert isinstance(board.get_piece((1,0)), Pawn) # Pedone bianco in a2
        assert board.get_piece((1,0)).color == Color.WHITE
        assert isinstance(board.get_piece((6,7)), Pawn) # Pedone nero in h7
        assert board.get_piece((6,7)).color == Color.BLACK
        assert board.get_piece((3,3)) is None # Casa vuota d4

    def test_move_piece(self):
        board = Board()
        pawn_a2_pos = (1,0) # a2
        pawn_a2 = board.get_piece(pawn_a2_pos)
        assert pawn_a2 is not None

        target_pos_a4 = (3,0) # a4
        captured = board.move_piece(pawn_a2_pos, target_pos_a4)

        assert captured is None
        assert board.get_piece(pawn_a2_pos) is None
        assert board.get_piece(target_pos_a4) == pawn_a2
        assert pawn_a2.position == target_pos_a4
        assert pawn_a2.has_moved is True