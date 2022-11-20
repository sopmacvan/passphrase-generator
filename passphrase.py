from secrets import choice
import string
import win32clipboard

with open('wordlists/eff_large_wordlist.txt_new') as f:
    # get all words from wordlist
    words = [word.strip() for word in f]


def generate_passphrase(n=3, delimiter='-', include_number=True, include_uppercase=True):
    """
    Create a passphrase with n number of words,
    separated by a delimiter, w/ or w/o a number and uppercase.

    :param n: int
    :param delimiter: str
    :param include_number: bool
    :param include_uppercase: bool
    :return: str
    """
    # choose n number of words
    passphrase = [choice(words) for _ in range(n)]

    # add a digit at the end of one random word if true
    if include_number:
        passphrase[choice(range(n))] += choice(string.digits)

    # put delimiter
    passphrase = delimiter.join(passphrase)

    # set first letter of each word to uppercase if true
    if include_uppercase:
        passphrase = passphrase.title()

    return passphrase


def copy_passphrase(text):
    """
    Copy passphrase to clipboard.

    :param text: str
    :return:
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
