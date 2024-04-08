import random
import string


def random_str(length, root_str: str = ""):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return f"{root_str}__{random_string}"
