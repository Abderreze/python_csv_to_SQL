import zipfile
import sys

def unzip_file(path_in, dir_out):
    """
    Décompresse tous les fichiers d'une archive ZIP dans un répertoire spécifié.

    ARGUMENTS
        path_in: (str), chemin vers le fichier ZIP à décompresser.
        dir_out: (str), répertoire où les fichiers seront extraits.

    RETOURNE
        (bool): True si la décompression réussit, False sinon.
    """
    try:
        with zipfile.ZipFile(path_in, 'r') as zip_ref:
            zip_ref.extractall(dir_out)
        return True
    except zipfile.BadZipfile:
        # Gestion d'une archive ZIP invalide
        sys.stderr.write(f"Err: le fichier {path_in} n'est pas un fichier ZIP valide")
        return False
    except FileNotFoundError:
        # Gestion d'un fichier introuvable
        sys.stderr.write(f"Err: Le fichier {path_in} n'a pas été trouvé")
        return False
    except Exception as e:
        # Gestion d'autres erreurs inattendues
        sys.stderr.write(f"Err. lors de la décompression: {e}")
        return False

