# game.py
"""Definisce la classe Game che gestisce la logica del gioco degli scacchi."""

from typing import List, Optional, Tuple

# Assumiamo che siano nello stesso pacchetto o PYTHONPATH
from .constants import Color, COMMANDS
from .board import Board
from .ui import UI
from .utils import parse_move, coords_to_algebraic, algebraic_to_coords
from .pieces import Piece # Import Piece per type hinting


class Game:
    """Gestisce lo stato e la logica di una partita di scacchi."""

    def __init__(self, ui: UI):
        """
        Inizializza una nuova partita.

        Args:
            ui (UI): L'oggetto UI per l'interazione con l'utente.
        """
        self.board = Board()
        self.ui = ui
        self.current_player = Color.WHITE # Il bianco inizia sempre
        self.move_history: List[str] = [] # Lista delle mosse in notazione algebrica
        self.game_started = False
        self.game_over = False
        self.winner: Optional[Color] = None

    def start_game(self):
        """Inizia una nuova partita."""
        if self.game_started and not self.game_over:
            self.ui.display_message("Una partita è già in corso. Usa /abbandona per terminarla prima.", level="warning")
            return

        self.board = Board() # Resetta la scacchiera
        self.current_player = Color.WHITE
        self.move_history = []
        self.game_started = True
        self.game_over = False
        self.winner = None
        self.ui.display_message("Nuova partita iniziata. Tocca al Bianco.", level="success")
        self.ui.display_board(self.board, self.current_player)

    def _switch_player(self):
        """Cambia il giocatore corrente."""
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

    def _add_move_to_history(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], piece: Piece, captured_piece: Optional[Piece]):
        """
        Aggiunge la mossa alla cronologia in notazione algebrica.
        Per lo Sprint 1: usa solo la notazione della casa di arrivo per i pedoni (es. "e4").

        Args:
            start_pos (Tuple[int, int]): Coordinate di partenza.
            end_pos (Tuple[int, int]): Coordinate di arrivo.
            piece (Piece): Il pezzo mosso.
            captured_piece (Optional[Piece]): Il pezzo catturato (se presente).
        """
        # TODO: Implementare la notazione algebrica completa (pezzo, cattura, scacco, etc.)
        # Per ora, per i pedoni, usiamo solo la casa di destinazione
        if isinstance(piece, piece.Pawn): # Assicurati che piece.Pawn sia corretto (dovrebbe essere solo Pawn)
             from .pieces import Pawn # Importa qui per evitare errore di riferimento
             if isinstance(piece, Pawn):
                 algebraic_move = coords_to_algebraic(end_pos)
                 if algebraic_move:
                     self.move_history.append(algebraic_move)
                 else:
                     # Fallback se la conversione fallisce (non dovrebbe accadere)
                     self.move_history.append(f"{coords_to_algebraic(start_pos)}-{coords_to_algebraic(end_pos)}")
        else:
             # Per altri pezzi (non nello sprint 1), faremo un placeholder
             start_alg = coords_to_algebraic(start_pos)
             end_alg = coords_to_algebraic(end_pos)
             if start_alg and end_alg:
                 self.move_history.append(f"{piece.get_symbol()}{start_alg}-{end_alg}") # Placeholder
             else:
                 self.move_history.append("Mossa Sconosciuta")


    def make_move(self, move_string: str) -> bool:
        """
        Tenta di eseguire una mossa data in notazione algebrica.

        Args:
            move_string (str): La mossa inserita dall'utente (es. "e4").

        Returns:
            bool: True se la mossa è stata eseguita con successo, False altrimenti.
        """
        if not self.game_started or self.game_over:
            self.ui.display_message("La partita non è attiva. Usa /gioca per iniziare.", level="warning")
            return False

        # 1. Parse della mossa: Traduce "e4" in ((start_row, start_col), (end_row, end_col))
        parsed_coords = parse_move(move_string, self.board, self.current_player)

        if parsed_coords is None:
            # Prova a vedere se è una notazione completa tipo "e2e4"
            if len(move_string) == 4:
                start_alg = move_string[:2]
                end_alg = move_string[2:]
                start_coords_direct = algebraic_to_coords(start_alg)
                end_coords_direct = algebraic_to_coords(end_alg)
                if start_coords_direct and end_coords_direct:
                    parsed_coords = (start_coords_direct, end_coords_direct)
                else:
                    self.ui.display_message(f"Mossa '{move_string}' non valida o non riconosciuta.", level="error")
                    return False
            else:
                 self.ui.display_message(f"Mossa '{move_string}' non valida o non riconosciuta.", level="error")
                 return False


        start_pos, end_pos = parsed_coords

        # 2. Validazione: Controlla se il pezzo esiste e appartiene al giocatore corrente
        piece_to_move = self.board.get_piece(start_pos)

        if piece_to_move is None:
            self.ui.display_message(f"Nessun pezzo trovato in {coords_to_algebraic(start_pos)}.", level="error")
            return False

        if piece_to_move.color != self.current_player:
            self.ui.display_message(f"Non è il tuo turno di muovere il pezzo in {coords_to_algebraic(start_pos)}.", level="error")
            return False

        # 3. Validazione specifica del pezzo: Chiede al pezzo se la mossa è valida
        # Nota: get_valid_moves per Pawn (Sprint 1) non include catture.
        # Dobbiamo assicurarci che la mossa richiesta sia tra quelle calcolate.
        # In futuro, parse_move dovrebbe gestire meglio la distinzione tra mosse e catture.
        valid_moves_for_piece = piece_to_move.get_valid_moves(self.board)

        # Controlla anche le mosse di cattura (anche se non implementate in get_valid_moves di Pawn)
        # Questo è un workaround per lo sprint 1 dove la specifica menziona solo movimento
        is_capture = self.board.get_piece(end_pos) is not None
        target_piece = self.board.get_piece(end_pos)

        # Controlli specifici per il pedone (Sprint 1 - solo movimento)
        from .pieces import Pawn
        if isinstance(piece_to_move, Pawn):
            if is_capture:
                 self.ui.display_message("La cattura con i pedoni non è implementata in questo sprint.", level="error")
                 return False
            if end_pos not in valid_moves_for_piece:
                 self.ui.display_message(f"Mossa non valida per il pedone da {coords_to_algebraic(start_pos)} a {coords_to_algebraic(end_pos)}.", level="error")
                 return False
        else:
            # Per altri pezzi (non nello sprint 1), assumiamo per ora che se parse_move l'ha data, è ok
            # TODO: Implementare validazione completa per tutti i pezzi
             self.ui.display_message("Solo le mosse dei pedoni sono implementate in questo sprint.", level="error")
             return False


        # 4. Esecuzione della mossa sulla scacchiera
        try:
            captured_piece = self.board.move_piece(start_pos, end_pos)
            # Nota: Nello sprint 1, captured_piece dovrebbe essere sempre None per i pedoni
            if captured_piece:
                 self.ui.display_message(f"Pezzo catturato: {captured_piece.get_symbol()} a {coords_to_algebraic(end_pos)}", level="info")

        except ValueError as e:
            # Questo errore non dovrebbe accadere se i controlli precedenti sono corretti
            self.ui.display_message(f"Errore durante l'esecuzione della mossa: {e}", level="error")
            return False

        # 5. Aggiornamento stato del gioco
        self._add_move_to_history(start_pos, end_pos, piece_to_move, captured_piece)
        self._switch_player()
        self.ui.display_board(self.board, self.current_player) # Mostra la scacchiera aggiornata

        # TODO: Controllare scacco, scacco matto, stallo
        # self._check_game_end_conditions()

        return True

    def handle_command(self, command: str):
        """
        Gestisce i comandi inseriti dall'utente (che iniziano con '/').

        Args:
            command (str): Il comando inserito (es. "/help").
        """
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
            self._handle_exit()
        else:
            self.ui.display_message(f"Comando '{command}' sconosciuto. Usa /help per la lista.", level="error")

    def _handle_resign(self):
        """Gestisce il comando /abbandona."""
        if not self.game_started or self.game_over:
            self.ui.display_message("Nessuna partita attiva da abbandonare.", level="warning")
            return

        if self.ui.get_confirmation("Sei sicuro di voler abbandonare la partita?"):
            self.game_over = True
            self.winner = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            self.ui.display_message(f"Partita terminata. {self.winner.name} vince per abbandono!", level="success")
        else:
            self.ui.display_message("Abbandono annullato.", level="info")

    def _handle_draw_offer(self):
        """Gestisce il comando /patta."""
        if not self.game_started or self.game_over:
            self.ui.display_message("Nessuna partita attiva per proporre la patta.", level="warning")
            return

        opponent_color = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        self.ui.display_message(f"Il giocatore {self.current_player.name} propone la patta.", level="info")

        # In un gioco a terminale 1vs1 sulla stessa macchina, la conferma è immediata
        if self.ui.get_confirmation(f"Giocatore {opponent_color.name}, accetti la patta?"):
            self.game_over = True
            self.winner = None # Patta
            self.ui.display_message("Patta accettata! La partita termina in pareggio.", level="success")
        else:
            self.ui.display_message("Proposta di patta rifiutata. Il gioco continua.", level="info")

    def _handle_exit(self):
        """Gestisce il comando /esci."""
        if self.ui.get_confirmation("Sei sicuro di voler uscire dal gioco?"):
            self.ui.display_message("Grazie per aver giocato a Scacchi! Arrivederci.", level="info")
            # Non impostiamo game_over qui, perché vogliamo che il loop principale termini
            return True # Segnala al loop principale di uscire
        else:
            self.ui.display_message("Uscita annullata.", level="info")
            return False # Segnala al loop principale di continuare

    def run(self):
        """Avvia il loop principale del gioco."""
        self.ui.display_welcome_message()
        # self.ui.get_player_name() # Chiede il nome, ma non lo usiamo attivamente per ora

        should_exit = False
        while not should_exit:
            prompt = f"{self.current_player.name} > " if self.game_started and not self.game_over else "> "
            user_input = self.ui.get_user_input(prompt)

            if not user_input: # Ignora input vuoto
                continue

            if user_input.startswith('/'):
                command = user_input.split()[0] # Prende solo il comando, ignora eventuali argomenti per ora
                if command == "/esci":
                    should_exit = self._handle_exit()
                else:
                    self.handle_command(command)
            elif self.game_started and not self.game_over:
                # Se non è un comando e il gioco è attivo, prova a interpretarlo come una mossa
                self.make_move(user_input)
            elif not self.game_started:
                 self.ui.display_message("Nessuna partita in corso. Usa /gioca per iniziare o /help per i comandi.", level="info")
            else: # Gioco finito
                 self.ui.display_message("La partita è terminata. Usa /gioca per una nuova partita o /esci.", level="info")

