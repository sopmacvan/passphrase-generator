import PySimpleGUI as sg
from pysqlitecipher import sqlitewrapper
from setup import setup_done
import pass_gen
import pass_vault


def authenticate():
    """Authenticate user by asking for password and check if it matches the master password."""
    while True:
        password = sg.popup_get_text('Enter your Master Password', password_char='*')

        # quit if user clicked 'cancel'
        if password is None:
            quit()

        # get hashed login and master password
        login_pass = sqlitewrapper.SqliteCipher.sha512Convertor(password)
        master_pass = sqlitewrapper.SqliteCipher.getVerifier('user/vault.db', checkSameThread=False)

        # check if hashed login and master password matches
        if login_pass == master_pass:
            return password
        else:
            sg.popup_error('Login failed!')


# ---------- USER INTERFACE ----------#

def create_menu_window(login_pass):
    """Create menu window which has the open vault, generate passphrase, and exit"""
    # ---------- WINDOW LAYOUT ----------#

    layout = [
        # Button for Vault
        [sg.Button('Open Vault', key='-PASS VAULT-', button_color=('black', '#F8EF00'), font=('Helvetica', 12),
                   size=(50, 2))],
        # Button for Generate Passphrase
        [sg.Button('Generate Passphrase', key='-PASS GEN-', button_color=('black', '#F8EF00'), font=('Helvetica', 12),
                   size=(50, 2))],
        # Button for Exit
        [sg.Button('Exit', key='-EXIT-', button_color=('white', '#Ff0000'), font=('Helvetica', 12),
                   size=(50, 2))],
    ]
    window = sg.Window('PG Menu', layout)

    # ---------- EVENT LOOP ----------#
    while True:
        event, values = window.read()
        # See if window was closed
        if event in (sg.WIN_CLOSED, '-EXIT-'):
            break
        if event == '-PASS VAULT-':
            vault = sqlitewrapper.SqliteCipher(dataBasePath="user/vault.db", checkSameThread=False, password=login_pass)

            pass_vault.create_vault_window(vault)
        if event == '-PASS GEN-':
            pass_gen.create_gen_window()
    # Close window
    window.close()


if __name__ == '__main__':
    sg.theme('DarkBlack')
    if setup_done():
        login_pass = authenticate()
        create_menu_window(login_pass)
    else:
        sg.popup("Please run setup.py first!", title='Missing components')
