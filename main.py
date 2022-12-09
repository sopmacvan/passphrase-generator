from passphrase import generate_passphrase
import pyperclip
import PySimpleGUI as sg

#----------- Sample -----------------#

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

    sg.theme('DarkBlack')

    # Define the window's layout
    layout = [
        # Custom exit button 
        #[sg.Button('x',key='-EXIT-')],
        # Passphrase Generator Top-Left Text
        [sg.Text('PASSPHRASE\nGENERATOR', background_color='#000000', text_color='#F8EF00', font=('Tomorrow',40,'bold'),size=(100,2))],
        # Initial Passphrase 
        [sg.Text(initial_passphrase, key='-PASSPHRASE-',background_color='#001819',border_width='32',text_color='#00F0FF',font=('Tomorrow',16),size=(100,1))],
        # Generate Password Button
        [sg.Button('Generate Password', key='-GENERATE-', button_color=('black','#F8EF00'), font=('Helvetica',16),size=(100,2))],
        # Copy Passphrase Button
        [sg.Button('Copy Password', key='-COPY-', button_color=('black','#F8EF00'), font=('Helvetica',16),size=(100,2))],

        [sg.Frame(title='Customize', background_color='#000000',font=('Tomorrow',20),
                  layout=[[sg.Column([
                    # Text: 
                      [sg.Text('Set word count',background_color='#000000',font=('Tomorrow',20))],
                      [sg.Text('Set delimiter',background_color='#000000',font=('Tomorrow',20))],
                      [sg.Text('Include number',background_color='#000000',font=('Tomorrow',20))],
                      [sg.Text('Include Uppercase',font=('Tomorrow',20))]
                  ]), sg.Column([
                    # Inputs & Checkbox
                      [sg.Input(size=(2, 1), default_text=fix_num(prev_settings.get('word_count', 3)),
                                key='-WORD COUNT-')],
                      [sg.Input(size=(2, 1), default_text=prev_settings.get('delimiter', '-'), key='-DELIMITER-')],
                      [sg.Checkbox('', default=prev_settings.get('include_number', True), key='-INCLUDE NUMBER-')],
                      [sg.Checkbox('', default=prev_settings.get('include_uppercase', True),
                                   key='-INCLUDE UPPERCASE-')],

                  ])]],
                  expand_x=True)],
        # Text:
        [sg.Text('Password History', enable_events=True, tooltip='Show/hide password history', key='-SHOW HISTORY-',font=('Tomorrow',20))],
        [sg.pin(sg.Column([
            # Listbox :
            [sg.Listbox(values=load_history(), size=(0, 5), font=('Tomorrow',16), expand_x=True, enable_events=True,
                        key='-PASSWORD HISTORY-')],
            # Clear History Button
            [sg.Button('Clear History', key='-CLEAR HISTORY-', button_color=('#F8EF00','black'),font=('Tomorrow',16),size=(100,1))]
        ],
            visible=False, expand_x=True, key='-COLUMN HISTORY-'), expand_x=True)],
    ]

    # UI: Set Window Size & BG Color
    return sg.Window('Passphrase Generator', layout,size=(430,850),background_color='#000000')

                    # UI: For borderless window

                    #default_element_size=(12, 1),
                    #text_justification='r',
                    #auto_size_text=False,
                    #auto_size_buttons=False,
                        #no_titlebar=True,
                        #grab_anywhere=True,
                    #default_button_element_size=(12, 1)

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

        # Event for exit button
        if event == '-EXIT-':
            window.close()

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

if __name__ == '__main__':
    main()