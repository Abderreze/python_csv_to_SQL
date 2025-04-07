import zipfile
import sys


def unzip_file(path_in, dir_out):
    """Unzips all files from a zip archive to a specified directory."""
    try:
        with zipfile.ZipFile(path_in, 'r') as zip_ref:
            zip_ref.extractall(dir_out)
        return True
    except zipfile.BadZipfile:
        sys.stderr.write(f"Err: le fichier {path_in} n'est pas un fichier ZIP valide")
        return False
    except FileNotFoundError:
        sys.stderr.write(f"Err: Le fichier {path_in} n'a pas été trouvé")
        return False
    except Exception as e:
        sys.stderr.write(f"Err. lors de la décompression: {e}")
        return False

