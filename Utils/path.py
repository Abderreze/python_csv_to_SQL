import os
import sys

def resource_path(relative_path):
    """Donne le chemin absolu à une ressource,
    permet la compilation avec pyinstaller et utilisation python directe."""
    if getattr(sys, 'frozen', False): # vérification pour voir si execution depuis .exe
        base_path = sys._MEIPASS # dossier temporaire pyinstaller
    else:
        base_path = os.path.abspath(".") # répértoire courant
    return os.path.join(base_path, relative_path)
