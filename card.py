import hashlib
from tqdm import tqdm
import logging
import multiprocessing as mp


def reverse_number(n):
    n = str(n)
    return n[::-1]


def check_hash(hash: str, card_number: str) -> bool:
    """Compares hash in the task with the hash of the card number

    Args:
        hash (str): hash in the task
        card_number (str): number of the bank card

    Returns:
        bool: result of comparison of two hashes
    """
    logging.info("Checking the hash")
    card_hash = hashlib.sha256(card_number.encode()).hexdigest()
    if hash == card_hash:
        return int(card_number)
    return 0


def get_card_number(
    hash: str, bins: list, last_numbs: str, core_number: int = mp.cpu_count()
) -> int:
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
    for j in bins:
        args.append((hash, f"{j}{000000}{last_numbs}"))
    for i in range(100000,1000000):
        for j in bins:
            args.append((hash, f"{j}{i}{last_numbs}"))
            i = reverse_number(i)
            args.append((hash, f"{j}{i}{last_numbs}"))
    with mp.Pool(processes=core_number) as p:
        for result in p.starmap(check_hash, tqdm(args, ncols=120, colour="green")):
            if result:
                p.terminate()
                logging.info("Card number got successfully")
                return result
    logging.info("Card number not got")
    return 0


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
        tmp = num * 2
        if tmp > 9:
            nums.append(tmp % 10 + tmp // 10)
        else:
            nums.append(tmp)
    res = 0
    for num in nums:
        res += num
    res = 10 - res % 10
    logging.info("Check the card number using the Luhn algorithm")
    return res == last
