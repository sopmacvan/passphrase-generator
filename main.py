import pass_gen
from login import authenticate
import PySimpleGUI as sg


def create_window_layout():
    # Define the window's layout
    layout = [
        [sg.Button('Open Vault', key='-PASS VAULT-')],
        [sg.Button('Generate Passphrase', key='-PASS GEN-')],
        [sg.Button('Exit', key='-EXIT-')],
    ]
    # UI: Set Window Size & BG Color
    return sg.Window('Passphrase Generator', layout)


def main():
    window = create_window_layout()

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
    sg.theme('DarkBlack')
    # authenticate()
    main()
