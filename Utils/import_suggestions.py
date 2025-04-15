import sys
import requests

def import_suggestions_file(file_url):
    """
    Télécharge un fichier de suggestions à partir d'une URL et l'enregistre localement.
    Args:
        file_url (str): L'URL du fichier à télécharger.
    Returns:
        bool: Retourne False en cas d'erreur, sinon rien n'est retourné.
    """
    if file_url:
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            with open("suggestions.csv", "wb") as f:
                f.write(response.content)

        except requests.exceptions.RequestException as e:
            sys.stderr.write(f"Err. lors du téléchargement du fichier suggestions: {e}")
            return False
    else:
        sys.stderr.write("URL pour le fichier trivia prenoms non configurée dans config.ini")
        return False
