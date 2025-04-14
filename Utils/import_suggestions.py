import sys
import requests

def import_suggestions_file(file_url):
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
