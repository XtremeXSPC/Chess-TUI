# ui.py
"""Gestisce l'interfaccia utente del gioco nel terminale."""

from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List, Optional, Tuple

from .constants import BOARD_SIZE, IDX_TO_COL, COMMANDS, Color, RICH_COLORS
from .board import Board
from .pieces import Piece # Import Piece per type hinting


class UI:
    """Definisce la configurazione e le funzioni per l'interfaccia utente del gioco."""

    def __init__(self):
        """Inizializza l'UI con impostazioni predefinite."""
        self._accent_color: str = "blue"
        self._white_square_color: str = "bright_white"
        self._black_square_color: str = "grey50" 
        self._white_piece_color: str = "bold white"
        self._black_piece_color: str = "bold black"
        
        self._visual_cell_width: int = 4
        self._visual_cell_height: int = 3

    def set_accent_color(self, accent_color: str):
        if accent_color in RICH_COLORS:
            self._accent_color = accent_color
        else:
            rprint(f"[bold red]Errore:[/bold red] Colore '{accent_color}' non valido. "
                   f"Il colore di accento rimane '{self._accent_color}'.")

    def get_accent_color(self) -> str:
        return self._accent_color

    def display_welcome_message(self):
        rprint(Panel(f"Benvenuto in [bold {self._accent_color}]Scacchi[/bold {self._accent_color}]!",
                     title="Scacchi Terminal Edition", border_style=self._accent_color))
        self.display_help_suggestion()

    def display_help_suggestion(self):
        rprint("Digita [bold cyan]/help[/bold cyan] per vedere i comandi disponibili.")

    def _create_multiline_text_block(self,
                                     center_line_content: str,
                                     block_width: int,
                                     padding_top: int,
                                     padding_bottom: int) -> str:
        """
        Helper per creare un blocco di testo multilinea con contenuto centrato verticalmente.
        `center_line_content` dovrebbe già essere formattato alla larghezza `block_width`.
        """
        lines = []
        empty_padding_line = " " * block_width
        for _ in range(padding_top):
            lines.append(empty_padding_line)
        lines.append(center_line_content)
        for _ in range(padding_bottom):
            lines.append(empty_padding_line)
        return "\n".join(lines)

    def _get_cell_symbol_and_style(self,
                                   piece: Optional[Piece],
                                   is_white_square: bool
                                   ) -> Tuple[str, str]:
        """Restituisce il simbolo del pezzo (o spazio) e lo stile Rich per una cella."""
        symbol = piece.get_symbol() if piece else " "
        
        bg_color = self._white_square_color if is_white_square else self._black_square_color
        
        style: str
        if piece:
            fg_color = self._white_piece_color if piece.color == Color.WHITE else self._black_piece_color
            style = f"{fg_color} on {bg_color}"
        else:
            style = f"on {bg_color}"
        return symbol, style

    def display_board(self, board: Board, current_player: Optional[Color] = None):
        """Mostra la scacchiera usando Rich, con celle visivamente più grandi."""
        table = Table.grid(expand=False)

        padding_vertical_top = (self._visual_cell_height - 1) // 2
        padding_vertical_bottom = self._visual_cell_height - 1 - padding_vertical_top
        
        row_label_display_width = 2  # Larghezza per etichette di riga "8 ", "1 "

        # --- RIGA DI INTESTAZIONE (ETICHETTE COLONNE E ANGOLO) ---
        header_row_elements = []

        # Angolo superiore sinistro
        empty_corner_center_line = " " * row_label_display_width
        corner_block_text = self._create_multiline_text_block(
            empty_corner_center_line, row_label_display_width,
            padding_vertical_top, padding_vertical_bottom
        )
        header_row_elements.append(Text(corner_block_text, style="dim"))

        # Etichette Colonne (a-h)
        for c_idx in range(BOARD_SIZE):
            col_char = IDX_TO_COL[c_idx]
            col_label_center_line = f"{col_char:^{self._visual_cell_width}}"
            col_block_text = self._create_multiline_text_block(
                col_label_center_line, self._visual_cell_width,
                padding_vertical_top, padding_vertical_bottom
            )
            header_row_elements.append(Text(col_block_text, style="dim"))
        table.add_row(*header_row_elements)

        # --- RIGHE DELLA SCACCHIERA (da 8 in alto a 1 in basso) ---
        for r_idx in range(BOARD_SIZE - 1, -1, -1):
            current_board_row_elements = []

            # Etichetta Riga (numero)
            row_label_char = str(r_idx + 1)
            row_label_center_line = f"{row_label_char:<{row_label_display_width}}"
            row_label_block_text = self._create_multiline_text_block(
                row_label_center_line, row_label_display_width,
                padding_vertical_top, padding_vertical_bottom
            )
            current_board_row_elements.append(Text(row_label_block_text, style="dim"))

            # Caselle della scacchiera per questa riga
            for c_idx in range(BOARD_SIZE):
                current_piece = board.get_piece((r_idx, c_idx))
                is_current_square_white = (r_idx + c_idx) % 2 != 0
                
                piece_symbol, cell_style = self._get_cell_symbol_and_style(
                    current_piece, is_current_square_white
                )

                cell_center_line = f"{piece_symbol:^{self._visual_cell_width}}"
                cell_block_text = self._create_multiline_text_block(
                    cell_center_line, self._visual_cell_width,
                    padding_vertical_top, padding_vertical_bottom
                )
                current_board_row_elements.append(Text(cell_block_text, style=cell_style))
            
            table.add_row(*current_board_row_elements)

        # Titolo del pannello
        title_text = "Scacchiera"
        if current_player:
            player_name_cap = current_player.name.capitalize()
            title_text += f" - Tocca a: [bold {current_player.value}]{player_name_cap}[/bold {current_player.value}]"
        
        rprint(Panel(table, title=title_text, border_style=self._accent_color, padding=(0,1)))

    def display_help(self):
        help_text_content = Text()
        help_text_content.append("Comandi disponibili:\n\n", style="bold")
        for command, description in COMMANDS.items():
            help_text_content.append(f"- {command}: ", style=f"bold {self.get_accent_color()}")
            help_text_content.append(f"{description}\n")
        help_text_content.append("\nUsa la notazione algebrica (es. 'e4' o 'e2e4') per le mosse.")
        rprint(Panel(help_text_content, title="Aiuto", border_style=self.get_accent_color()))

    def display_message(self, message: str, level: str = "info"):
        color_map = {
            "info": self.get_accent_color(), "error": "red",
            "warning": "yellow", "success": "green",
        }
        selected_color = color_map.get(level.lower(), "white") 
        
        prefix_map = {
            "error": "Errore", "warning": "Attenzione", "success": "Successo"
        }
        prefix_text = prefix_map.get(level.lower())
        
        if prefix_text:
            rprint(f"[bold {selected_color}]{prefix_text}:[/bold {selected_color}] {message}")
        else: 
            rprint(f"[{selected_color}]{message}[/{selected_color}]")

    def get_confirmation(self, prompt: str) -> bool:
        while True:
            rprint(f"[bold {self.get_accent_color()}]{prompt} (s/n):[/bold {self.get_accent_color()}] ", end="")
            response = input().lower().strip()
            if response in ['s', 'si', 'sì']:
                return True
            if response in ['n', 'no']: 
                return False
            self.display_message("Risposta non valida. Per favore inserisci 's' o 'n'.", level="warning")

    def display_moves(self, move_history: List[str]):
         if not move_history:
             self.display_message("Nessuna mossa è stata ancora giocata.", level="info")
             return

         move_panel_content = Text()
         move_panel_content.append("Cronologia Mosse:\n\n", style="bold")
         move_number = 1
         for i in range(0, len(move_history), 2):
             white_move = move_history[i]
             black_move = move_history[i+1] if (i+1) < len(move_history) else ""
             move_panel_content.append(f"{move_number}. {white_move:<7} {black_move}\n")
             move_number += 1
         rprint(Panel(move_panel_content, title="Mosse Giocate", border_style=self.get_accent_color()))

    def get_user_input(self, prompt: str = "Inserisci comando o mossa") -> str:
        rprint(f"[{self.get_accent_color()}]{prompt}[/{self.get_accent_color()}]", end="")
        return input().strip()