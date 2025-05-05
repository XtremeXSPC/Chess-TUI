# main.py
"""Punto di ingresso principale per il gioco Scacchi."""

import sys
import argparse

# Assumiamo che le classi siano definite nei moduli corrispondenti
# all'interno dello stesso pacchetto (es. 'scacchi')
try:
    from .ui import UI
    from .game import Game
    from .constants import COMMANDS # Importa COMMANDS per l'help da argomento
except ImportError:
    # Fallback se eseguito come script singolo (meno probabile con la struttura a pacchetto)
    print("Errore: Assicurati che il gioco sia installato o eseguito come modulo (es. python -m scacchi).")
    print("Importazione fallback dei moduli locali...")
    from ui import UI
    from game import Game
    from constants import COMMANDS


def display_help_from_args():
    """Mostra l'aiuto basato sui comandi definiti."""
    print("Scacchi Terminal Edition - Un semplice gioco di scacchi nel terminale.")
    print("\nComandi disponibili:")
    for command, description in COMMANDS.items():
        print(f"  {command:<15} {description}")
    print("\nUsa la notazione algebrica standard (es. 'e4') per le mosse durante il gioco.")

def main():
    """Avvia e gestisce il gioco degli scacchi."""

    parser = argparse.ArgumentParser(description="Scacchi Terminal Edition", add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Mostra questo messaggio di aiuto ed esci')
    # Potremmo aggiungere altri argomenti qui in futuro (es. colori UI)

    # Parsa solo gli argomenti conosciuti per permettere l'esecuzione senza argomenti
    args, unknown = parser.parse_known_args()

    if args.help:
        display_help_from_args()
        sys.exit(0) # Esce dopo aver mostrato l'aiuto

    # Inizializza l'interfaccia utente e il gioco
    ui = UI()
    # ui.set_accent_color("cyan") # Imposta un colore diverso se vuoi

    game = Game(ui)

    # Avvia il loop principale del gioco
    try:
        game.run()
    except KeyboardInterrupt:
        ui.display_message("\nUscita forzata rilevata. Arrivederci!", level="warning")
    except Exception as e:
        ui.display_message(f"\nErrore inaspettato: {e}", level="error")
        # Considera di loggare l'errore completo per il debug
        # import traceback
        # traceback.print_exc()
    finally:
        # Codice di pulizia eventuale
        pass


if __name__ == "__main__":
    # Questo blocco viene eseguito se main.py è lanciato direttamente come script.
    # Per una struttura a pacchetto, l'esecuzione tipica sarebbe `python -m scacchi`
    # che eseguirebbe __main__.py (se esiste) o importerebbe il pacchetto.
    # Manteniamo questo per compatibilità e test diretti.
    main()

