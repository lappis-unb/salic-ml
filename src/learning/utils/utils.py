import string
import sys


def is_valid_pronac(pronac):
    MAX_PRONAC_LEN = 7
    if not isinstance(pronac, str) or len(pronac) > MAX_PRONAC_LEN:
        return False

    VALID_DIGITS = string.digits + "xX"
    for digit in pronac:
        if digit not in VALID_DIGITS:
            return False
    return True


def debug(message):
    print("\n")
    print("{}".format(message))
    sys.stdout.flush()
