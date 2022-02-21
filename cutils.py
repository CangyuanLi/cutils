from collections.abc import Iterable, Sequence
import math

def contains(x: Iterable, elements) -> bool:
    return any(elem in x for elem in elements)

def chunk_list(lst: list, n: int) -> list:
    """Splits a list into n sized chunk

    Args:
        lst (list): a list
        n (int): number of items in chunk

    Yields:
        list: A list of lists of size n, with last list
        being of size len(lst) mod n | n
    """
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def find_last_index(x: Sequence, target):
    for i in range(len(x) - 1, -1, -1):
        if x[i] == target:
            return i

    return None

def maxmod(n: int, k: int) -> int:
    """Find the divisor that maximizes
    the remainder

    Args:
        n (int): numerator
        k (int): denominator

    Returns:
        int: divisor that maximized n mod k 
    """
    max = 0
    for i in range(1, k, -1):
        xx = n % i
        if max < xx:
            max = xx
        if i < max:
            break

    return max

def get_factors(n):
    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(int(n // i))

    return factors
