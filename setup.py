from pysqlitecipher import sqlitewrapper
import PySimpleGUI as sg
from pathlib import Path


# TODO: add more restrictions for password creation such as symbols, numbers, uppercase
def create_master_password():
    """
    Create strong master password.
    """

    def length_greater_than_7(password):
        # check if password length is greater than 7
        return len(password) > 7

    while True:
        password = sg.popup_get_text('Setup: Create your Master Password', title='Setup')
        if password is None:
            quit()
        if not length_greater_than_7(password):
            sg.popup('Password length must be 8 or greater.')
            continue

        # confirm password
        if sg.popup_ok_cancel(
                "IMPORTANT:\nMaster password CANNOT be restored. If you lose it, you lose access to all accounts"
                " saved in your vault. \n\nClick OK to proceed."
        , title='Reminder') == 'OK':
            return password


def setup_done():
    """Check if setup is done by checking if vault.db exists w/c should have been created after setup."""
    vault = Path("user/vault.db")
    return vault.exists()


def setup():
    """
    1. Create master password.
    2. Create database in user folder and use the master password to protect it.
    3. Create accounts table.
    :return:
    """
    if setup_done():
        sg.popup('Setup is already done.')
    else:
        # create master password
        password = create_master_password()

        # create database and protect w/ master password
        obj = sqlitewrapper.SqliteCipher(dataBasePath="user/vault.db", checkSameThread=False, password=password)

        # create accounts table
        col_list = [["name", "TEXT"], ["username", "TEXT"], ["password", "TEXT"], ]
        obj.createTable('accounts', col_list, makeSecure=False, commit=True)

        sg.popup('Setup done!')


if __name__ == '__main__':
    sg.theme('DarkBlack')
    setup()
