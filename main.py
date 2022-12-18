import pass_gen
import PySimpleGUI as sg
from pysqlitecipher import sqlitewrapper
from setup import setup_done


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
            print('Login SUCCESSFUL')
            break
        else:
            print('Login FAILED')
            sg.popup_error('Login FAILED!!')


def create_menu_window():
    """Create menu window which has the open vault, generate passphrase, and exit"""
    # Define the window's layout
    layout = [
        [sg.Button('Open Vault', key='-PASS VAULT-')],
        [sg.Button('Generate Passphrase', key='-PASS GEN-')],
        [sg.Button('Exit', key='-EXIT-')],
    ]
    return sg.Window('Passphrase Generator', layout)


def main():
    window = create_menu_window()

    # Event Loop
    while True:
        event, values = window.read()
        # See if window was closed
        if event in (sg.WIN_CLOSED, '-EXIT-'):
            break
        if event == '-PASS VAULT-':
            pass
        if event == '-PASS GEN-':
            pass_gen.create()
    # Close window
    window.close()


if __name__ == '__main__':
    if setup_done():
        sg.theme('DarkBlack')
        authenticate()
        main()
    else:
        sg.popup("Please run setup.py first.")
