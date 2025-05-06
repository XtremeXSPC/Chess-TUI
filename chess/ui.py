# ui.py
"""Gestisce l'interfaccia utente del gioco nel terminale."""

from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List, Tuple, Optional

from .constants import BOARD_SIZE, IDX_TO_COL, COMMANDS, Color
from .board import Board
from .pieces import Piece

class UI:
    """Definisce la configurazione e le funzioni per l'interfaccia utente del gioco."""

    def __init__(self):
        """Inizializza l'UI con impostazioni predefinite."""
        self._accent_color: str = "blue"
        self._white_square_color: str = "bright_white"
        self._black_square_color: str = "grey50"
        self._white_piece_color: str = "white"
        self._black_piece_color: str = "black"
        # Definiamo la larghezza delle celle dei pezzi per coerenza
        self._cell_char_width = 5 # Esempio: "  P  " (2 spazi, 1 pezzo, 2 spazi)

    def set_accent_color(self, accent_color: str):
        """Imposta il colore di accento per l'UI."""
        RICH_COLORS: set[str] = {
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
            "grey50",
        }
        if accent_color in RICH_COLORS:
            self._accent_color = accent_color
        else:
            rprint(f"[bold red]Errore:[/bold red] Colore '{accent_color}' non valido. Uso '{self._accent_color}'.")

    def get_accent_color(self) -> str:
        """Restituisce il colore di accento corrente."""
        return self._accent_color

    def display_welcome_message(self):
        """Mostra il messaggio di benvenuto."""
        rprint(Panel(f"Benvenuto in [bold {self._accent_color}]Scacchi[/bold {self._accent_color}]!",
                     title="Scacchi Terminal Edition", border_style=self._accent_color))

    def get_player_name(self) -> str:
        """Chiede e restituisce il nome del giocatore."""
        name = input("Inserisci il tuo nome: ")
        rprint(f"Ciao [bold {self._accent_color}]{name}[/bold {self._accent_color}]! "
               f"Usa [bold cyan]/help[/bold cyan] per vedere i comandi.")
        return name

    def display_board(self, board: Board, current_player: Optional[Color] = None):
        """
        Mostra la scacchiera usando Rich, con layout migliorato.
        - Spazio tra numeri di riga e scacchiera.
        - Pezzi centrati verticalmente nelle celle (alte 2 "sotto-righe").

        Args:
            board (Board): L'oggetto scacchiera da visualizzare.
            current_player (Optional[Color]): Il giocatore di turno, per indicarlo.
        """
        table = Table.grid(expand=False)

        # Calcola il padding per centrare orizzontalmente il pezzo
        # Se il pezzo è 1 carattere, e la cella è larga 5, servono 2 spazi per lato.
        piece_padding_char = " "
        padding_len = (self._cell_char_width - 1) // 2
        side_padding = piece_padding_char * padding_len
        # Assicura che la larghezza totale sia _cell_char_width, anche se il pezzo fosse più largo (non previsto qui)
        # o se _cell_char_width è pari.
        # Per larghezza 5 e pezzo 1: "  P  " -> side_padding = "  "
        # Per larghezza 4 e pezzo 1: " P " -> side_padding = " " (padding_len = 1), un lato avrà uno spazio in più se necessario.
        # Semplifichiamo: assumiamo che il pezzo sia sempre 1 carattere.
        
        # Linea vuota per la parte superiore/inferiore della cella, con la larghezza definita
        empty_cell_line = piece_padding_char * self._cell_char_width

        # Intestazioni colonne (a-h)
        # Ogni intestazione è larga _cell_char_width e alta 2 "sotto-righe"
        column_headers = [
            Text(f"{side_padding}{IDX_TO_COL[c]}{side_padding}\n{empty_cell_line}", style="dim")
            for c in range(BOARD_SIZE)
        ]
        
        # Angolo superiore sinistro (per etichette riga) - larghezza 2, altezza 2 "sotto-righe"
        top_left_corner = Text("  \n  ", style="dim")
        # Intestazione per la colonna di separazione - larghezza 2, altezza 2 "sotto-righe"
        separator_header = Text("  \n  ", style="dim")

        table.add_row(top_left_corner, separator_header, *column_headers)

        for r in range(BOARD_SIZE - 1, -1, -1): # Itera dalla riga 7 alla 0
            row_cells = []
            for c in range(BOARD_SIZE):
                piece = board.get_piece((r, c))
                is_white_square = (r + c) % 2 != 0

                square_bg_color = self._white_square_color if is_white_square else self._black_square_color
                piece_symbol_display = piece.get_symbol() if piece else " "
                
                piece_style = f"bold {self._white_piece_color if piece and piece.color == Color.WHITE else self._black_piece_color} on {square_bg_color}"
                if not piece: # Stile per case vuote, solo sfondo
                    piece_style = f"on {square_bg_color}"

                # Costruzione della cella (alta 2 "sotto-righe", larga _cell_char_width)
                # Pezzo nella seconda "sotto-riga" per migliore centratura verticale
                line_with_piece  = f"{side_padding}{piece_symbol_display}{side_padding}"
                # Aggiusta la lunghezza se _cell_char_width è dispari e side_padding*2 + 1 non fa _cell_char_width
                # Questo assicura che la linea con il pezzo abbia la larghezza corretta
                if len(line_with_piece) < self._cell_char_width:
                    line_with_piece += piece_padding_char * (self._cell_char_width - len(line_with_piece))


                cell_text_content = f"{empty_cell_line}\n{line_with_piece}"
                
                cell_content = Text(cell_text_content, style=piece_style)
                row_cells.append(cell_content)

            # Etichetta riga (numero) - es. "8 ", larga 2 caratteri, alta 2 "sotto-righe"
            row_label_text = f"{r + 1:<2}" # Allinea a sinistra, padding con spazi se < 2 cifre
            row_label = Text(f"{row_label_text}\n  ", style="dim")
            
            # Cella di separazione per questa riga (tra numero e scacchiera)
            # Larga 2 caratteri, alta 2 "sotto-righe"
            separator_cell = Text("  \n  ", style=f"on {self._black_square_color if (r % 2 == 0) else self._white_square_color}")
            # Per rendere la colonna di separazione meno invadente, potremmo darle uno sfondo neutro
            # o provare a farla "trasparente" (difficile con Table.grid).
            # Per ora, le do uno sfondo alternato come se fosse parte della scacchiera,
            # oppure uno sfondo fisso:
            separator_cell = Text("  \n  ") # Sfondo di default del terminale

            table.add_row(row_label, separator_cell, *row_cells)

        title = "Scacchiera"
        if current_player:
            title += f" - Tocca al [bold {current_player.value}]{current_player.name}[/bold {current_player.value}]"
        
        rprint(Panel(table, title=title, border_style=self._accent_color, padding=(0,0))) # Padding del panel a 0


    def display_help(self):
        """Mostra l'elenco dei comandi disponibili."""
        help_text = "[bold]Comandi disponibili:[/bold]\n\n"
        for command, description in COMMANDS.items():
            help_text += f"- [bold cyan]{command}[/bold cyan]: {description}\n"
        help_text += "\nUsa la notazione algebrica standard (es. 'e4', 'Cf3') per le mosse."
        rprint(Panel(help_text, title="Aiuto", border_style="cyan"))

    def display_message(self, message: str, level: str = "info"):
        """Mostra un messaggio all'utente."""
        color_map = {
            "info": self._accent_color, "error": "red",
            "warning": "yellow", "success": "green",
        }
        color = color_map.get(level, "white")
        prefix = f"[{level.capitalize()}]: " if level != "info" else ""
        rprint(f"[bold {color}]{prefix}{message}[/bold {color}]")

    def get_confirmation(self, prompt: str) -> bool:
        """Chiede conferma all'utente (sì/no)."""
        while True:
            response = input(f"{prompt} (s/n): ").lower().strip()
            if response == 's': return True
            if response == 'n': return False
            self.display_message("Risposta non valida. Per favore inserisci 's' o 'n'.", level="warning")

    def display_moves(self, move_history: List[str]):
         """Mostra la cronologia delle mosse."""
         if not move_history:
             self.display_message("Nessuna mossa è stata ancora giocata.", level="info")
             return
         move_text = "[bold]Cronologia Mosse:[/bold]\n\n"
         move_number = 1
         for i in range(0, len(move_history), 2):
             white_move = move_history[i]
             black_move = move_history[i+1] if (i+1) < len(move_history) else ""
             move_text += f"{move_number}. {white_move:<6} {black_move}\n"
             move_number += 1
         rprint(Panel(move_text, title="Mosse Giocate", border_style=self._accent_color))

    def get_user_input(self, prompt: str = "Inserisci comando o mossa") -> str:
        """Ottiene l'input dall'utente."""
        return input(f"{prompt}: ").strip()
