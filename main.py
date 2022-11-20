from passphrase import generate_passphrase, copy_passphrase
import PySimpleGUI as sg


# ---------- MISCELLANEOUS ----------#
def fix_num(n):
    # use 3 as default if n is not a  number
    try:
        n = int(n)
    except ValueError:
        n = 3
    # Set word limit of 3-10
    n = 3 if n < 3 else n
    n = 10 if n > 10 else n

    return n


# ---------- CUSTOMIZATION SETTINGS ----------#
def save_settings(settings, values):
    settings['word_count'] = values['-WORD COUNT-'].get()
    settings['delimiter'] = values['-DELIMITER-'].get()
    settings['include_number'] = values['-INCLUDE NUMBER-'].get()
    settings['include_uppercase'] = values['-INCLUDE UPPERCASE-'].get()


# ---------- PASSWORD HISTORY ----------#
def load_history():
    with open('user/history.txt', 'r') as f:
        return f.readlines()


def append_history(passphrase):
    with open('user/history.txt', 'a') as f:
        f.write(f'{passphrase}\n')


def clear_history():
    with open('user/history.txt', 'w') as f:
        f.write('')


# ---------- USER INTERFACE AND EVENT LOOP ----------#

def create_window_layout(prev_settings):
    initial_passphrase = generate_passphrase(fix_num(prev_settings.get('word_count', 3)),
                                             prev_settings.get('delimiter', '-'),
                                             prev_settings.get('include_number', True),
                                             prev_settings.get('include_uppercase', True))
    append_history(initial_passphrase)

    # Define the window's layout
    layout = [
        [sg.Text(initial_passphrase, key='-PASSPHRASE-')],
        [sg.Button('Generate Passphrase', key='-GENERATE-')],
        [sg.Button('Copy Passphrase', key='-COPY-')],

        [sg.Frame(title='Customize',
                  layout=[[sg.Column([
                      [sg.Text('Set word count')],
                      [sg.Text('Set delimiter')],
                      [sg.Text('Include number')],
                      [sg.Text('Include Uppercase')]
                  ]), sg.Column([
                      [sg.Input(size=(2, 1), default_text=prev_settings.get('word_count', 3), key='-WORD COUNT-')],
                      [sg.Input(size=(2, 1), default_text=prev_settings.get('delimiter', '-'), key='-DELIMITER-')],
                      [sg.Checkbox('', default=prev_settings.get('include_number', True), key='-INCLUDE NUMBER-')],
                      [sg.Checkbox('', default=prev_settings.get('include_uppercase', True),
                                   key='-INCLUDE UPPERCASE-')],

                  ])]],
                  expand_x=True)],
        [sg.Text('Password History', enable_events=True, tooltip='Show/hide password history', key='-SHOW HISTORY-')],
        [sg.pin(sg.Column([
            [sg.Listbox(values=load_history(), size=(0, 3), expand_x=True, enable_events=True,
                        key='-PASSWORD HISTORY-')],
            [sg.Button('Clear Password', key='-CLEAR HISTORY-')]
        ],
            visible=False, expand_x=True, key='-COLUMN HISTORY-'), expand_x=True)],

    ]

    return sg.Window('Passphrase Generator', layout)


def main():
    settings = sg.UserSettings(filename='user/settings.json', autosave=True)

    window = create_window_layout(settings)
    # Event Loop
    while True:
        event, values = window.read()
        # See if window was closed
        if event == sg.WIN_CLOSED:
            save_settings(settings, window.key_dict)
            break

        # Generate a passphrase if user clicks the generate button
        if event == '-GENERATE-':
            n = fix_num(values['-WORD COUNT-'])

            passphrase = generate_passphrase(n,
                                             values['-DELIMITER-'],
                                             values['-INCLUDE NUMBER-'],
                                             values['-INCLUDE UPPERCASE-'])

            append_history(passphrase)
            window['-PASSWORD HISTORY-'].update(load_history())
            window['-PASSPHRASE-'].update(passphrase)
            window['-WORD COUNT-'].update(n)

        # Copy passphrase if user clicks the copy button
        if event == '-COPY-':
            copy_passphrase(window['-PASSPHRASE-'].get())

        # Show/hide password history
        if event == '-SHOW HISTORY-':
            visible = False if window['-COLUMN HISTORY-'].visible else True
            window['-COLUMN HISTORY-'].update(visible=visible)

        # Copy selected passphrase from password history if user clicks one
        if event == '-PASSWORD HISTORY-':
            copy_passphrase(window['-PASSWORD HISTORY-'].get()[0])

        # Clear history
        if event == '-CLEAR HISTORY-':
            clear_history()
            window['-PASSWORD HISTORY-'].update([])

    # Close window
    window.close()


if __name__ == '__main__':
    main()
