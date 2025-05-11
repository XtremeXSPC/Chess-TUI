# game.py
"""Definisce la classe Game che gestisce la logica del gioco degli scacchi."""

from typing import List, Optional, Tuple

from .constants import Color
from .board import Board
from .ui import UI
from .utils import parse_move as parse_algebraic_abbreviated, coords_to_algebraic, algebraic_to_coords
from .pieces import Piece, Pawn


class Game:
    """Gestisce lo stato e la logica di una partita di scacchi."""

    def __init__(self, ui: UI):
        self.board = Board()
        self.ui = ui
        self.current_player = Color.WHITE
        self.move_history: List[str] = []
        self.game_started = False
        self.game_over = False
        self.winner: Optional[Color] = None

    def start_game(self):
        if self.game_started and not self.game_over:
            self.ui.display_message("Una partita è già in corso. Usa /abbandona per terminarla prima.", level="warning")
            return
        self.board = Board()
        self.current_player = Color.WHITE
        self.move_history = []
        self.game_started = True
        self.game_over = False
        self.winner = None
        self.ui.display_message("Nuova partita iniziata. Tocca al Bianco.", level="success")
        self.ui.display_board(self.board, self.current_player)

    def _switch_player(self):
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

    def _add_move_to_history(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                             piece: Piece, captured_piece: Optional[Piece]):
        if isinstance(piece, Pawn):
            algebraic_move = coords_to_algebraic(end_pos)
            if algebraic_move:
                self.move_history.append(algebraic_move)
            else:
                self.move_history.append(f"{coords_to_algebraic(start_pos)}-{coords_to_algebraic(end_pos)}")
        else:
            start_alg = coords_to_algebraic(start_pos)
            end_alg = coords_to_algebraic(end_pos)
            if start_alg and end_alg:
                capture_indicator = "x" if captured_piece else "-"
                self.move_history.append(f"{piece.get_symbol()}{start_alg}{capture_indicator}{end_alg}")
            else:
                self.move_history.append("Mossa Sconosciuta")

    def _parse_user_move_input(self, move_string: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Tenta di parsare l'input dell'utente in coordinate di mossa.
        Prova prima il formato abbreviato (es. "e4"), poi il formato completo (es. "e2e4").
        Restituisce (start_coords, end_coords) o None.
        """
        # Tenta prima il parsing abbreviato (es. "e4")
        parsed_coords = parse_algebraic_abbreviated(move_string, self.board, self.current_player)
        if parsed_coords:
            return parsed_coords

        # Se fallisce, tenta il formato "e2e4"
        if len(move_string) == 4 and move_string[:2].isalnum() and move_string[2:].isalnum():
            start_alg, end_alg = move_string[:2], move_string[2:]
            start_coords_direct = algebraic_to_coords(start_alg)
            end_coords_direct = algebraic_to_coords(end_alg)
            if start_coords_direct and end_coords_direct:
                return (start_coords_direct, end_coords_direct)
            else:
                self.ui.display_message(f"Formato mossa '{move_string}' non valido (coordinate non corrette).", level="error")
                return None
        
        self.ui.display_message(f"Mossa '{move_string}' non riconosciuta o formato non valido.", level="error")
        return None

    def _validate_piece_and_move(self, piece_to_move: Optional[Piece], start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """
        Valida se il pezzo esiste, appartiene al giocatore corrente, e se la mossa è valida.
        Per lo Sprint 1, gestisce solo pedoni e le loro mosse di avanzamento.
        Restituisce True se valido, False altrimenti (e stampa messaggi di errore).
        """
        if piece_to_move is None:
            self.ui.display_message(f"Nessun pezzo trovato in {coords_to_algebraic(start_pos)}.", level="error")
            return False

        if piece_to_move.color != self.current_player:
            self.ui.display_message(f"Non è il tuo turno di muovere il pezzo in {coords_to_algebraic(start_pos)} ({piece_to_move.color.name}). È il turno di {self.current_player.name}.", level="error")
            return False

        if isinstance(piece_to_move, Pawn):
            valid_pawn_moves = piece_to_move.get_valid_moves(self.board)
            target_piece_at_end = self.board.get_piece(end_pos)

            if end_pos not in valid_pawn_moves:
                moves_alg = [coords_to_algebraic(m) for m in valid_pawn_moves if m is not None]
                self.ui.display_message(f"Mossa non valida per il pedone da {coords_to_algebraic(start_pos)} a {coords_to_algebraic(end_pos)}. Mosse possibili: {moves_alg}.", level="error")
                return False
            if target_piece_at_end is not None:
                self.ui.display_message("I pedoni non possono muovere su una casa occupata (le catture non sono implementate).", level="error")
                return False
        else:
            self.ui.display_message("Solo le mosse dei pedoni sono implementate in questo sprint.", level="error")
            return False
        
        return True

    def make_move(self, move_string: str) -> bool:
        """Tenta di eseguire una mossa data in notazione algebrica."""
        if not self.game_started or self.game_over:
            self.ui.display_message("La partita non è attiva. Usa /gioca per iniziare.", level="warning")
            return False

        parsed_coords = self._parse_user_move_input(move_string)
        if not parsed_coords:
            return False # Messaggio di errore già gestito da _parse_user_move_input

        start_pos, end_pos = parsed_coords
        piece_to_move = self.board.get_piece(start_pos)

        if not self._validate_piece_and_move(piece_to_move, start_pos, end_pos):
            return False # Messaggio di errore già gestito da _validate_piece_and_move
        
        # Asserzione per MyPy, dato che _validate_piece_and_move controlla non-None
        assert piece_to_move is not None 

        try:
            captured_piece = self.board.move_piece(start_pos, end_pos)
            if captured_piece: # Non dovrebbe accadere per pedoni Sprint 1
                 self.ui.display_message(f"Pezzo catturato: {captured_piece.get_symbol()} a {coords_to_algebraic(end_pos)} (Logica imprevista per Sprint 1)", level="warning")
        except ValueError as e:
            self.ui.display_message(f"Errore durante l'esecuzione della mossa: {e}", level="error")
            return False

        self._add_move_to_history(start_pos, end_pos, piece_to_move, captured_piece)
        self._switch_player()
        self.ui.display_board(self.board, self.current_player)
        # TODO: Controllare scacco, scacco matto, stallo
        return True

    def handle_command(self, command: str):
        """Gestisce i comandi dell'utente (che iniziano con '/')."""
        if command == "/help":
            self.ui.display_help()
        elif command == "/gioca": 
            self.start_game()
        elif command == "/scacchiera":
            if not self.game_started:
                self.ui.display_message("Nessuna partita in corso. Usa /gioca per iniziare.", level="info")
            else:
                self.ui.display_board(self.board, self.current_player)
        elif command == "/abbandona":
            self._handle_resign()
        elif command == "/patta": 
            self._handle_draw_offer()
        elif command == "/mosse": 
            self.ui.display_moves(self.move_history)
        elif command == "/esci": 
            pass # Gestito da _process_user_input nel loop run
        else:
            self.ui.display_message(f"Comando '{command}' sconosciuto. Usa /help per la lista.", level="error")

    def _handle_resign(self):
        if not self.game_started or self.game_over:
            self.ui.display_message("Nessuna partita attiva da abbandonare.", level="warning")
            return
        if self.ui.get_confirmation("Sei sicuro di voler abbandonare la partita?"):
            self.game_over = True
            self.winner = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            self.ui.display_message(f"Partita terminata. {self.winner.name.capitalize()} vince per abbandono!", level="success")
        else:
            self.ui.display_message("Abbandono annullato.", level="info")

    def _handle_draw_offer(self):
        if not self.game_started or self.game_over:
            self.ui.display_message("Nessuna partita attiva per proporre la patta.", level="warning")
            return
        opponent_color = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        self.ui.display_message(f"Il giocatore {self.current_player.name.capitalize()} propone la patta.", level="info")
        if self.ui.get_confirmation(f"Giocatore {opponent_color.name.capitalize()}, accetti la patta?"):
            self.game_over = True
            self.winner = None
            self.ui.display_message("Patta accettata! La partita termina in pareggio.", level="success")
        else:
            self.ui.display_message("Proposta di patta rifiutata. Il gioco continua.", level="info")

    def _request_exit(self) -> bool:
        """Chiede conferma per uscire e restituisce True se l'utente conferma."""
        if self.ui.get_confirmation("Sei sicuro di voler uscire dal gioco?"):
            self.ui.display_message("Grazie per aver giocato a Scacchi! Arrivederci.", level="info")
            return True
        self.ui.display_message("Uscita annullata.", level="info")
        return False

    def _process_user_input(self, user_input: str) -> bool:
        """
        Processa l'input dell'utente.
        Restituisce True se il gioco deve terminare (comando /esci confermato).
        """
        if not user_input:
            return False # Continua il loop

        if user_input.startswith('/'):
            command = user_input.split()[0]
            if command == "/esci":
                return self._request_exit() # Potrebbe terminare il gioco
            else:
                self.handle_command(command)
        elif self.game_started and not self.game_over:
            self.make_move(user_input)
        elif not self.game_started:
            self.ui.display_message("Nessuna partita in corso. Usa /gioca per iniziare o /help.", level="info")
        else:  # Gioco finito
            self.ui.display_message("La partita è terminata. Usa /gioca per una nuova partita o /esci.", level="info")
        
        return False # Non terminare il gioco (a meno che /esci non lo abbia fatto)


    def run(self):
        """Avvia il loop principale del gioco."""
        self.ui.display_welcome_message()

        should_exit = False
        while not should_exit:
            player_name_display = self.current_player.name.capitalize()
            prompt = f"{player_name_display} > " if self.game_started and not self.game_over else "Scacchi > "
            user_input = self.ui.get_user_input(prompt).strip()
            
            should_exit = self._process_user_input(user_input)