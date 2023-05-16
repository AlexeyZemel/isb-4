#4006234246b4fd2b2833d740927ab20465afad862c74b1a88ec0869bde5c836c|Mastercard|Дебетовая|Альфа-банк|0254|sha256|
import hashlib
import tqdm 
import json
import logging
import multiprocessing as mp 


def check_hash(hash: str, card_number: str) -> bool:
    """Compares hash in the task with the hash of the card number

    Args:
        hash (str): hash in the task
        card_number (str): number of the bank card

    Returns:
        bool: result of comparison of two hashes
    """
    logging.info("Checking the hash")
    return hashlib.sha256(card_number.encode()).hexdigest() == hash


def get_card_number(hash: str, bins: list, last_numbs: str, core_number: int = mp.cpu_count()) -> int:
    """Selects the card number

    Args:
        hash (str): hash in the task
        bins (list): bins of the cards
        last_numbs (str): last 4 numbers of the card
        core_number (int): number of processor cores

    Returns: 
        int: card number or 0 if failed
    """
    args = []
    for i in range(1000000):
        for j in bins:
            args.append((hash, f"{j}{i}{last_numbs}"))
    with mp.Pool(processes=core_number) as p:
        for res in p.starmap(check_hash, tqdm(args, ncols=120)):
            if res:
                p.terminate()
                return res
    return 0


def read_file(file_name: str) -> str:
    """Reads the file

    Args:
        file_name(str): name of the file
    
    Returns:
        str: data in the file
    """
    try:
        with open(file_name, 'r') as f:
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
        with open(file_name, 'w') as f:
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
        with open(file_name, 'r') as f:
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


def luhn(card_number: str) -> bool:
    """Checking the card number using the Luhn algorithm

    Args: 
        card_number(srt): number of the card 

    Returns: 
        bool: is the card number real
    """
    nums = []
    card = list(map(int, card_number))
    last = card[15]
    card.pop()
    for num in card: 
        tmp = num*2
        if tmp>9:
            nums.append(tmp%10 + tmp//10)
        else:
            nums.append(tmp)
    res = 0
    for num in nums:
        res += num
    res = 10 - res % 10
    return res == last