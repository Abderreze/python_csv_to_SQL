import configparser

def set_setting(config_path, section, variable, value):
    """Met à jour un paramètre dans un fichier config.

    ARGUMENTS
        config_path: str, chemin du fichier config
        section: str, catégorie de la variable à mettre à jour
        variable: str, la variable à mettre à jour
        value: str, la valeur par laquelle remplacer l'ancienne

    RETURNS
        None
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set(section, variable, value)

    with open(config_path, "w") as configfile:
        config.write(configfile)
