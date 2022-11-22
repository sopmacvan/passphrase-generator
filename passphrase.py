from secrets import choice
import string

# get all words from wordlists
f1 = open('wordlists/eff_large_wordlist.txt_new')
f2 = open('wordlists/eff_short_wordlist_1.txt_new')
f3 = open('wordlists/eff_short_wordlist_2_0.txt_new')

words = [word.strip() for word in f1] + \
        [word.strip() for word in f2] + \
        [word.strip() for word in f3]
f1.close()
f2.close()
f3.close()


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
