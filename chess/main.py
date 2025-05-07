# main.py
"""Punto di ingresso principale per il gioco Scacchi."""

import sys
import argparse
import traceback

from .ui import UI
from .game import Game
from .constants import COMMANDS


def display_help_from_args():
    """Mostra l'aiuto basato sui comandi definiti, per l'uso da riga di comando."""
    print("Scacchi Terminal Edition - Un semplice gioco di scacchi nel terminale.")
    print("\nOpzioni riga di comando:")
    print("  -h, --help-args     Mostra questo messaggio di aiuto ed esci.")
    print("\nComandi disponibili all'interno del gioco (iniziano con '/'):")
    for command, description in COMMANDS.items():
        print(f"  {command:<15} {description}")
    print("\nMosse di Gioco:")
    print("  Usa la notazione algebrica per le mosse (es. 'e4' o 'e2e4').")
    print("\nPer eseguire il gioco:")
    print("  Naviga nella directory che contiene la cartella 'scacchi' e usa:")
    print("  python -m scacchi")


def run_game():
    """Avvia e gestisce il gioco degli scacchi."""

    # Parser per gli argomenti specifici dell'applicazione, prima di avviare l'UI del gioco
    parser = argparse.ArgumentParser(description="Scacchi Terminal Edition", add_help=False)
    parser.add_argument(
        '-h', '--help-args',
        action='store_true',
        help='Mostra aiuto per argomenti da linea di comando ed esci.'
    )

    args, unknown_args = parser.parse_known_args()

    if args.help_args:
        display_help_from_args()
        sys.exit(0)
    
    if unknown_args:
        print(f"Argomenti non riconosciuti: {unknown_args}")
        display_help_from_args()
        sys.exit(1)


    ui = UI()
    game = Game(ui)

    try:
        game.run()
    except KeyboardInterrupt:
        ui.display_message("\nUscita forzata rilevata. Arrivederci!", level="warning")
    except Exception as e:
        ui.display_message(f"\nErrore inaspettato: {e}", level="error")
        ui.display_message("Consultare il traceback qui sotto per dettagli:", level="error")
        traceback.print_exc()


if __name__ == "__main__":
    # Questo blocco viene eseguito se main.py è lanciato direttamente
    # o tramite `python -m scacchi.main`.
    run_game()