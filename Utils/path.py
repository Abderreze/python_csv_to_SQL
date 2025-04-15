import os
import sys

def resource_path(relative_path):
    """
    Retourne le chemin absolu vers une ressource, compatible avec PyInstaller.

    ARGUMENTS
        relative_path: (str), chemin relatif de la ressource.

    RETOURNE
        (str): chemin absolu vers la ressource.
    """
    if getattr(sys, 'frozen', False):  # Vérifie si le script est exécuté depuis un exécutable .exe
        base_path = sys._MEIPASS  # Dossier temporaire utilisé par PyInstaller
    else:
        base_path = os.path.abspath(".")  # Répertoire courant
    return os.path.join(base_path, relative_path)
