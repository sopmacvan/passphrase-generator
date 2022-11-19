from passphrase import generate_passphrase, copy_passphrase
import PySimpleGUI as sg

# Define the window's layout
layout = [
    [sg.Text(generate_passphrase(), key='-PASSPHRASE-')],
    [sg.Button('Generate Passphrase', key='-GENERATE-')],
    [sg.Button('Copy Passphrase', key='-COPY-')],

    [sg.Frame(title='Customize',
              layout=[[sg.Column([
                  [sg.Text('Set word count')],
                  [sg.Text('Set delimiter')],
                  [sg.Text('Include number')],
                  [sg.Text('Include Uppercase')]
              ]), sg.Column([
                  [sg.Input(size=(2, 1), default_text='3', key='-WORD COUNT-')],
                  [sg.Input(size=(2, 1), default_text='-', key='-DELIMITER-')],
                  [sg.Checkbox('', default=True, key='-INCLUDE NUMBER-')],
                  [sg.Checkbox('', default=True, key='-INCLUDE UPPERCASE-')],

              ])]],
              expand_x=True)],

    [sg.Text('Password History')],

]

# Create the window
window = sg.Window('Passphrase Generator', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event in (sg.WINDOW_CLOSED, 'Quit'):
        break

    # Generate a passphrase if user clicks the generate button
    if event == '-GENERATE-':
        n = int(values['-WORD COUNT-'])
        delimiter = values['-DELIMITER-']
        include_number = values['-INCLUDE NUMBER-']
        include_uppercase = values['-INCLUDE UPPERCASE-']
        passphrase = generate_passphrase(n, delimiter, include_number, include_uppercase)

        window['-PASSPHRASE-'].update(passphrase)

    # Copy the passphrase if user clicks the copy button
    if event == '-COPY-':
        passphrase = layout[0][0].DisplayText
        copy_passphrase(passphrase)

# Close the window
window.close()
