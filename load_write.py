import logging
import json


def read_file(file_name: str) -> str:
    """Reads the file

    Args:
        file_name(str): name of the file

    Returns:
        str: data in the file
    """
    try:
        with open(file_name, "r") as f:
            data = f.read()
        logging.info("Read the data successfully")
    except OSError as err:
        logging.info("Read the data is failed")
        raise err
    return data


def write_file(data: str, file_name: str) -> None:
    """Writes the data in the file

    Args:
        data(str): data for writting
        file_name(str): name of the file where to write
    """
    try:
        with open(file_name, "w") as f:
            f.write(data)
        logging.info("Write the data successfully")
    except OSError as err:
        logging.info("Write the data is failed")
        raise err


def read_list(file_name: str) -> list:
    """Read the data in the file and writes it into list

    Args:
        file_name(str): name of the file

    Returns:
        list: list with the read data
    """
    data = []
    try:
        with open(file_name, "r") as f:
            data = f.readlines()
            data = list(map(int, data))
        logging.info("Read the data successfuly")
    except OSError as err:
        logging.info("Read the data is failed")
        raise err
    return data


def load_settings(json_file: str) -> dict:
    """Loads a settings file into the program.

    Args:
        json_file (str): The path to the json file with the settings.

    Returns:
        dict: dictionary with settings
    """
    settings = None
    try:
        with open(json_file) as json_file:
            settings = json.load(json_file)
        logging.info("Settings loaded successfully")
    except OSError as err:
        logging.info("Settings not loaded")
        raise err
    return settings
