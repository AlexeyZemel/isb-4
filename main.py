#4006234246b4fd2b2833d740927ab20465afad862c74b1a88ec0869bde5c836c|Mastercard|Дебетовая|Альфа-банк|0254|sha256|
import hashlib
import tqdm 
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