# main.py
"""Punto di ingresso principale per il gioco Scacchi."""

import sys
import argparse

# Importazioni relative, assumeranno che il gioco sia eseguito come modulo
from .ui import UI
from .game import Game
from .constants import COMMANDS # Importa COMMANDS per l'help da argomento


def display_help_from_args():
    """Mostra l'aiuto basato sui comandi definiti."""
    print("Scacchi Terminal Edition - Un semplice gioco di scacchi nel terminale.")
    print("\nComandi disponibili:")
    for command, description in COMMANDS.items():
        print(f"  {command:<15} {description}")
    print("\nUsa la notazione algebrica standard (es. 'e4') per le mosse durante il gioco.")
    print("\nPer eseguire il gioco, naviga nella directory che contiene la cartella 'chess' e usa:")
    print("  python -m chess")
    print("Oppure:")
    print("  python -m chess.main")


def run_game():
    """Avvia e gestisce il gioco degli scacchi."""

    parser = argparse.ArgumentParser(description="Scacchi Terminal Edition", add_help=False)
    # Definiamo l'argomento help qui in modo che non entri in conflitto con l'help interno del gioco
    parser.add_argument('-h', '--help-args', action='store_true', help='Mostra questo messaggio di aiuto ed esci (argomenti linea di comando).')

    args, _ = parser.parse_known_args()

    if args.help_args:
        display_help_from_args()
        sys.exit(0)

    ui = UI()
    game = Game(ui)

    try:
        game.run() # Il comando /help interno al gioco è gestito da game.run()
    except KeyboardInterrupt:
        ui.display_message("\nUscita forzata rilevata. Arrivederci!", level="warning")
    except Exception as e:
        ui.display_message(f"\nErrore inaspettato: {e}", level="error")
        import traceback
        traceback.print_exc() # Utile per il debug

# Questa funzione 'main' è quella che verrà chiamata da __main__.py
# o se si esegue specificamente `python -m chess.main`
if __name__ == "__main__":
    # Questo blocco viene eseguito se main.py è lanciato con `python -m chess.main`.
    # Se viene eseguito direttamente come `python chess/main.py`, le importazioni relative falliranno prima.
    run_game()
