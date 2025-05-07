# ui.py
"""Gestisce l'interfaccia utente del gioco nel terminale."""

from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List, Optional

from .constants import BOARD_SIZE, IDX_TO_COL, COMMANDS, Color, RICH_COLORS
from .board import Board
# Piece non è direttamente usato qui, ma è utile per type hinting se si passassero pezzi singoli
# from .pieces import Piece


class UI:
    """Definisce la configurazione e le funzioni per l'interfaccia utente del gioco."""

    def __init__(self):
        """Inizializza l'UI con impostazioni predefinite."""
        self._accent_color: str = "blue"
        self._white_square_color: str = "bright_white"
        self._black_square_color: str = "grey50" 
        self._white_piece_color: str = "bold white"
        self._black_piece_color: str = "bold black"
        
        # Dimensioni visive per ogni cella della scacchiera
        # Usare numeri dispari per un migliore centraggio di un singolo carattere
        self._visual_cell_width: int = 6  # Larghezza di ogni cella in caratteri
        self._visual_cell_height: int = 3 # Altezza di ogni cella in righe di testo

    def set_accent_color(self, accent_color: str):
        """
        Imposta il colore di accento per l'UI, se valido.
        Altrimenti, mantiene il colore precedente e stampa un messaggio.
        """
        if accent_color in RICH_COLORS:
            self._accent_color = accent_color
        else:
            rprint(f"[bold red]Errore:[/bold red] Colore '{accent_color}' non valido. "
                   f"Il colore di accento rimane '{self._accent_color}'.")

    def get_accent_color(self) -> str:
        """Restituisce il colore di accento corrente."""
        return self._accent_color

    def display_welcome_message(self):
        """Mostra il messaggio di benvenuto."""
        rprint(Panel(f"Benvenuto in [bold {self._accent_color}]Scacchi[/bold {self._accent_color}]!",
                     title="Scacchi Terminal Edition", border_style=self._accent_color))
        self.display_help_suggestion()

    def display_help_suggestion(self):
        """Suggerisce il comando /help."""
        rprint(f"Digita [bold cyan]/help[/bold cyan] per vedere i comandi disponibili.")


    def display_board(self, board: Board, current_player: Optional[Color] = None):
        """
        Mostra la scacchiera usando Rich, con celle visivamente più grandi.
        """
        table = Table.grid(expand=False)

        # Calcola il padding verticale per centrare il contenuto nelle celle alte _visual_cell_height
        padding_vertical_top = (self._visual_cell_height - 1) // 2
        padding_vertical_bottom = self._visual_cell_height - 1 - padding_vertical_top
        
        empty_line_for_cell = " " * self._visual_cell_width

        # --- INTESTAZIONI COLONNE (a-h) ---
        column_header_items = []
        # Angolo superiore sinistro (vuoto, per allineare le etichette di riga)
        top_left_corner_text_parts = ["  " * self._visual_cell_height] # 2 spazi di larghezza
        column_header_items.append(
            Text("\n".join(["  "] * self._visual_cell_height), style="dim")
        )


        for c_idx in range(BOARD_SIZE):
            col_char = IDX_TO_COL[c_idx]
            col_label_line_content = f"{col_char:^{self._visual_cell_width}}" # Lettera centrata
            
            current_col_label_text_parts = []
            for _ in range(padding_vertical_top):
                current_col_label_text_parts.append(empty_line_for_cell)
            current_col_label_text_parts.append(col_label_line_content)
            for _ in range(padding_vertical_bottom):
                current_col_label_text_parts.append(empty_line_for_cell)
            
            column_header_items.append(Text("\n".join(current_col_label_text_parts), style="dim"))
        table.add_row(*column_header_items)

        # --- RIGHE DELLA SCACCHIERA (8 a 1) ---
        for r_idx in range(BOARD_SIZE - 1, -1, -1):
            row_render_elements = []

            # Etichetta riga (numero) - centrata verticalmente
            row_label_char = str(r_idx + 1)
            # Larghezza etichetta riga (es. 2 caratteri: "8 ")
            row_label_width = 2 
            empty_row_label_line = " " * row_label_width
            row_label_content_line = f"{row_label_char:<{row_label_width}}" # Numero allineato a sx

            row_label_text_parts = []
            for _ in range(padding_vertical_top):
                row_label_text_parts.append(empty_row_label_line)
            row_label_text_parts.append(row_label_content_line)
            for _ in range(padding_vertical_bottom):
                row_label_text_parts.append(empty_row_label_line)
            
            row_render_elements.append(Text("\n".join(row_label_text_parts), style="dim"))

            # Caselle della scacchiera per questa riga
            for c_idx in range(BOARD_SIZE):
                piece = board.get_piece((r_idx, c_idx))
                is_white_square = (r_idx + c_idx) % 2 != 0

                square_bg_color = self._white_square_color if is_white_square else self._black_square_color
                piece_symbol_on_board = piece.get_symbol() if piece else " "
                
                # Stile del pezzo (colore) e sfondo della casella
                current_cell_style = ""
                if piece:
                    piece_fg_color = self._white_piece_color if piece.color == Color.WHITE else self._black_piece_color
                    current_cell_style = f"{piece_fg_color} on {square_bg_color}"
                else:
                    current_cell_style = f"on {square_bg_color}"

                # Costruzione del contenuto multilinea della cella
                cell_text_lines = []
                # Linea con il pezzo (o spazio), centrato orizzontalmente
                line_with_piece_content = f"{piece_symbol_on_board:^{self._visual_cell_width}}"

                for _ in range(padding_vertical_top):
                    cell_text_lines.append(empty_line_for_cell)
                cell_text_lines.append(line_with_piece_content)
                for _ in range(padding_vertical_bottom):
                    cell_text_lines.append(empty_line_for_cell)
                
                cell_final_text_block = "\n".join(cell_text_lines)
                row_render_elements.append(Text(cell_final_text_block, style=current_cell_style))
            
            table.add_row(*row_render_elements)

        title_text = "Scacchiera"
        if current_player:
            player_name_cap = current_player.name.capitalize()
            title_text += f" - Tocca a: [bold {current_player.value}]{player_name_cap}[/bold {current_player.value}]"
        
        rprint(Panel(table, title=title_text, border_style=self._accent_color, padding=(0,1)))


    def display_help(self):
        """Mostra l'elenco dei comandi disponibili."""
        help_text_content = Text()
        help_text_content.append("Comandi disponibili:\n\n", style="bold")
        for command, description in COMMANDS.items():
            help_text_content.append(f"- {command}: ", style=f"bold {self.get_accent_color()}")
            help_text_content.append(f"{description}\n")
        help_text_content.append("\nUsa la notazione algebrica (es. 'e4' o 'e2e4') per le mosse.")
        rprint(Panel(help_text_content, title="Aiuto", border_style=self.get_accent_color()))

    def display_message(self, message: str, level: str = "info"):
        """Mostra un messaggio all'utente con un livello di enfasi."""
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
        """Chiede conferma all'utente (sì/no)."""
        while True:
            rprint(f"[bold {self.get_accent_color()}]{prompt} (s/n):[/bold {self.get_accent_color()}] ", end="")
            response = input().lower().strip()
            if response in ['s', 'si', 'sì']: return True
            if response in ['n', 'no']: return False
            self.display_message("Risposta non valida. Per favore inserisci 's' o 'n'.", level="warning")

    def display_moves(self, move_history: List[str]):
         """Mostra la cronologia delle mosse."""
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
        """Ottiene l'input dall'utente, visualizzando il prompt con stile."""
        rprint(f"[{self.get_accent_color()}]{prompt}[/{self.get_accent_color()}]", end="")
        return input().strip()