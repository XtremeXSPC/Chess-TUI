# __main__.py
"""
Punto di ingresso eseguibile per il pacchetto 'scacchi'.

Questo permette di eseguire il pacchetto usando `python -m scacchi`.
"""

# Importa la funzione principale dal modulo main.py
from .main import run_game

if __name__ == "__main__":
    run_game()