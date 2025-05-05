# ui.py
"""Gestisce l'interfaccia utente del gioco nel terminale."""

from rich import print as rprint # Usa un alias per evitare conflitti con la funzione print standard
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List, Tuple, Optional

# Assumiamo che 'constants.py', 'board.py', 'pieces.py' siano nello stesso pacchetto o PYTHONPATH
from .constants import BOARD_SIZE, IDX_TO_COL, COMMANDS, Color
from .board import Board
from .pieces import Piece

class UI:
    """Definisce la configurazione e le funzioni per l'interfaccia utente del gioco."""

    def __init__(self):
        """Inizializza l'UI con impostazioni predefinite."""
        self._accent_color: str = "blue" # Colore predefinito per evidenziazioni
        self._white_square_color: str = "bright_white" # Colore per case bianche
        self._black_square_color: str = "grey50" # Colore per case nere (usa un grigio)
        self._white_piece_color: str = "white" # Colore pezzi bianchi
        self._black_piece_color: str = "black" # Colore pezzi neri

    def set_accent_color(self, accent_color: str):
        """Imposta il colore di accento per l'UI."""
        # (Codice esistente da main.py - validazione colore)
        RICH_COLORS: set[str] = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
            "grey50", # Aggiunto per le case nere
        }
        if accent_color in RICH_COLORS:
            self._accent_color = accent_color
        else:
            # Potremmo voler gestire l'errore in modo diverso qui, magari loggare e usare default
            rprint(f"[bold red]Errore:[/bold red] Colore '{accent_color}' non valido. Uso '{self._accent_color}'.")
            # raise ValueError(f"Invalid accent color '{accent_color}'.") # Rimosso per non bloccare

    def get_accent_color(self) -> str:
        """Restituisce il colore di accento corrente."""
        return self._accent_color

    def display_welcome_message(self):
        """Mostra il messaggio di benvenuto."""
        rprint(Panel(f"Benvenuto in [bold {self._accent_color}]Scacchi[/bold {self._accent_color}]!",
                     title="Scacchi Terminal Edition", border_style=self._accent_color))

    def get_player_name(self) -> str:
        """Chiede e restituisce il nome del giocatore."""
        # Usiamo input standard, ma potremmo usare rich.prompt in futuro
        name = input("Inserisci il tuo nome: ")
        rprint(f"Ciao [bold {self._accent_color}]{name}[/bold {self._accent_color}]! "
               f"Usa [bold cyan]/help[/bold cyan] per vedere i comandi.")
        return name # Anche se non lo usiamo subito, potrebbe servire

    def display_board(self, board: Board, current_player: Optional[Color] = None):
        """
        Mostra la scacchiera usando Rich, con colori per case e pezzi.

        Args:
            board (Board): L'oggetto scacchiera da visualizzare.
            current_player (Optional[Color]): Il giocatore di turno, per indicarlo.
        """
        table = Table.grid(expand=False)
        # Aggiungi colonne per le lettere (a-h) in alto
        table.add_row("", *[f"[dim]{IDX_TO_COL[c]}[/dim]" for c in range(BOARD_SIZE)])

        for r in range(BOARD_SIZE - 1, -1, -1): # Itera dalla riga 7 alla 0 (visualizzazione da 8 a 1)
            row_cells = []
            for c in range(BOARD_SIZE):
                piece = board.get_piece((r, c))
                is_white_square = (r + c) % 2 != 0 # Determina il colore della casa

                square_bg_color = self._white_square_color if is_white_square else self._black_square_color
                piece_symbol = " " # Spazio per case vuote
                piece_style = ""

                if piece:
                    piece_symbol = piece.get_symbol()
                    piece_color = self._white_piece_color if piece.color == Color.WHITE else self._black_piece_color
                    # Assicurati che il colore del pezzo sia leggibile sullo sfondo della casa
                    # Rich gestisce questo abbastanza bene, ma potremmo aggiungere logica se necessario
                    piece_style = f"bold {piece_color} on {square_bg_color}"
                else:
                    # Per case vuote, usa solo il colore di sfondo
                    piece_style = f"on {square_bg_color}"

                # Aggiungi uno spazio prima e dopo il simbolo per padding
                cell_content = Text(f" {piece_symbol} ", style=piece_style)
                row_cells.append(cell_content)

            # Aggiungi il numero di riga all'inizio
            table.add_row(f"[dim]{r + 1}[/dim]", *row_cells)

        title = "Scacchiera"
        if current_player:
            title += f" - Tocca al [bold {current_player.value}]{current_player.name}[/bold {current_player.value}]"

        rprint(Panel(table, title=title, border_style=self._accent_color, padding=(0, 1)))

    def display_help(self):
        """Mostra l'elenco dei comandi disponibili."""
        help_text = "[bold]Comandi disponibili:[/bold]\n\n"
        for command, description in COMMANDS.items():
            help_text += f"- [bold cyan]{command}[/bold cyan]: {description}\n"
        help_text += "\nUsa la notazione algebrica standard (es. 'e4', 'Cf3') per le mosse."
        rprint(Panel(help_text, title="Aiuto", border_style="cyan"))

    def display_message(self, message: str, level: str = "info"):
        """
        Mostra un messaggio all'utente (info, errore, successo).

        Args:
            message (str): Il testo del messaggio.
            level (str): Il tipo di messaggio ('info', 'error', 'warning', 'success').
        """
        color_map = {
            "info": self._accent_color,
            "error": "red",
            "warning": "yellow",
            "success": "green",
        }
        color = color_map.get(level, "white")
        prefix = f"[{level.capitalize()}]: " if level != "info" else ""
        rprint(f"[bold {color}]{prefix}{message}[/bold {color}]")

    def get_confirmation(self, prompt: str) -> bool:
        """
        Chiede conferma all'utente (sì/no).

        Args:
            prompt (str): La domanda da porre.

        Returns:
            bool: True se l'utente conferma, False altrimenti.
        """
        while True:
            response = input(f"{prompt} (s/n): ").lower().strip()
            if response == 's':
                return True
            if response == 'n':
                return False
            self.display_message("Risposta non valida. Per favore inserisci 's' o 'n'.", level="warning")

    def display_moves(self, move_history: List[str]):
         """
         Mostra la cronologia delle mosse.

         Args:
             move_history (List[str]): Lista delle mosse in notazione algebrica.
         """
         if not move_history:
             self.display_message("Nessuna mossa è stata ancora giocata.", level="info")
             return

         move_text = "[bold]Cronologia Mosse:[/bold]\n\n"
         move_number = 1
         for i in range(0, len(move_history), 2):
             white_move = move_history[i]
             black_move = move_history[i+1] if (i+1) < len(move_history) else ""
             move_text += f"{move_number}. {white_move:<6} {black_move}\n" # Allinea le mosse
             move_number += 1

         rprint(Panel(move_text, title="Mosse Giocate", border_style=self._accent_color))

    def get_user_input(self, prompt: str = "Inserisci comando o mossa") -> str:
        """
        Ottiene l'input dall'utente.

        Args:
            prompt (str): Il messaggio da mostrare all'utente.

        Returns:
            str: L'input dell'utente ripulito.
        """
        return input(f"{prompt}: ").strip()

