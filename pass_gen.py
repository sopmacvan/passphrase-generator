import PySimpleGUI as sg
from secrets import choice
import pyperclip
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


# ---------- MISCELLANEOUS ----------#

def generate(n=3, delimiter='-', include_number=True, include_uppercase=True):
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


def fix_num(n):
    # use 3 as default if n is not a  number
    min_limit = 3
    max_limit = 10
    try:
        n = int(n)
    except ValueError:
        return min_limit
    # Set word limit of 3-10
    n = min_limit if n < min_limit else n
    n = max_limit if n > max_limit else n
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


# ---------- USER INTERFACE ----------#

def create_gen_window():
    """Create passphrase generator window w/c can generate passphrase, copy passphrase, and
    has customizations and history"""

    settings = sg.UserSettings(filename='user/settings.json', autosave=True)

    initial_passphrase = generate(fix_num(settings.get('word_count', 3)),
                                  settings.get('delimiter', '-'),
                                  settings.get('include_number', True),
                                  settings.get('include_uppercase', True))
    append_history(initial_passphrase)

    # ---------- WINDOW LAYOUT ----------#

    layout = [
        # Custom exit button
        # [sg.Button('x',key='-EXIT-')],
        # Passphrase Generator Top-Left Text
        [sg.Text('PASSPHRASE\nGENERATOR', background_color='#000000', text_color='#F8EF00',
                 font=('Tomorrow', 40, 'bold'), size=(100, 2))],
        # Initial Passphrase
        [sg.Text(initial_passphrase, key='-PASSPHRASE-', background_color='#001819', border_width='32',
                 text_color='#00F0FF', font=('Tomorrow', 16), size=(100, 1))],
        # Generate Password Button
        [sg.Button('Generate Password', key='-GENERATE-', button_color=('black', '#F8EF00'), font=('Helvetica', 16),
                   size=(100, 2))],
        # Copy Passphrase Button
        [sg.Button('Copy Password', key='-COPY-', button_color=('black', '#F8EF00'), font=('Helvetica', 16),
                   size=(100, 2))],

        [sg.Frame(title='Customize', background_color='#000000', font=('Tomorrow', 20),
                  layout=[
                      # Text + Inputs and Checkbox:
                      [sg.Text('Set word count', background_color='#000000', font=('Tomorrow', 20), size=(20, 1)),
                       sg.Input(size=(2, 1), default_text=fix_num(settings.get('word_count', 3)),
                                key='-WORD COUNT-')],
                      [sg.Text('Set delimiter', background_color='#000000', font=('Tomorrow', 20), size=(20, 1)),
                       sg.Input(size=(2, 1), default_text=settings.get('delimiter', '-'), key='-DELIMITER-')],
                      [sg.Text('Include number', background_color='#000000', font=('Tomorrow', 20), size=(20, 1)),
                       sg.Checkbox('', default=settings.get('include_number', True), key='-INCLUDE NUMBER-')],
                      [sg.Text('Include Uppercase', font=('Tomorrow', 20), size=(20, 1)),
                       sg.Checkbox('', default=settings.get('include_uppercase', True),
                                   key='-INCLUDE UPPERCASE-')]
                  ],
                  expand_x=True)],
        # Text:
        [sg.Text('Password History', enable_events=True, tooltip='Show/hide password history', key='-SHOW HISTORY-',
                 font=('Tomorrow', 20))],
        [sg.pin(sg.Column([
            # Listbox :
            [sg.Listbox(values=load_history(), size=(0, 5), font=('Tomorrow', 16), expand_x=True, enable_events=True,
                        key='-PASSWORD HISTORY-')],
            # Clear History Button
            [sg.Button('Clear History', key='-CLEAR HISTORY-', button_color=('#F8EF00', 'black'), font=('Tomorrow', 16),
                       size=(100, 1))]
        ],
            visible=False, expand_x=True, key='-COLUMN HISTORY-'), expand_x=True)],

    ]

    # UI: Set Window Size & BG Color
    window = sg.Window('Pass Generator', layout, size=(430, 850), background_color='#000000')

    # UI: For borderless window

    # default_element_size=(12, 1),
    # text_justification='r',
    # auto_size_text=False,
    # auto_size_buttons=False,
    # no_titlebar=True,
    # grab_anywhere=True,
    # default_button_element_size=(12, 1)

    # ---------- EVENT LOOP ----------#

    while True:
        event, values = window.read()
        # See if window was closed
        if event == sg.WIN_CLOSED:
            save_settings(settings, window.key_dict)
            break

        # Generate a passphrase if user clicks the generate button
        if event == '-GENERATE-':
            n = fix_num(values['-WORD COUNT-'])

            passphrase = generate(n,
                                  values['-DELIMITER-'],
                                  values['-INCLUDE NUMBER-'],
                                  values['-INCLUDE UPPERCASE-'])

            append_history(passphrase)
            window['-PASSWORD HISTORY-'].update(load_history())
            window['-PASSPHRASE-'].update(passphrase)
            window['-WORD COUNT-'].update(n)

        # Copy passphrase to clipboard if user clicks the copy button
        if event == '-COPY-':
            passphrase = window['-PASSPHRASE-'].get()
            pyperclip.copy(passphrase)

        # Show/hide password history
        if event == '-SHOW HISTORY-':
            visible = False if window['-COLUMN HISTORY-'].visible else True
            window['-COLUMN HISTORY-'].update(visible=visible)

        # Copy selected passphrase to clipboard if user clicks one
        if event == '-PASSWORD HISTORY-':
            try:
                passphrase = window['-PASSWORD HISTORY-'].get()[0]
                pyperclip.copy(passphrase)
            except IndexError:
                pass
        # Clear history
        if event == '-CLEAR HISTORY-':
            clear_history()
            window['-PASSWORD HISTORY-'].update([])

    # Close window
    window.close()
