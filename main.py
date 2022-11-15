import PySimpleGUI as sg

# create customize description (left part)
customize_description = [
    [sg.Text('Set word count')],
    [sg.Text('Set delimiter')],
    [sg.Text('Include number')],
    [sg.Text('Include Uppercase')]
]

# create customize input (right part)
customize_input = [
    [sg.Input(size=(2, 1))],
    [sg.Input(size=(2, 1))],
    [sg.Checkbox('', default=True)],
    [sg.Checkbox('', default=True)],

]

# Create customize frame w/c contains both description and input
customize_frame = sg.Frame(title='Customize',
                           layout=[[sg.Column(customize_description), sg.Column(customize_input)]],
                           expand_x=True)

# Define the window's layout
layout = [
    [sg.Text("My-Generated-Passphrase1")],
    [sg.Button('Generate Passphrase')],
    [sg.Button('Copy Passphrase')],

    [customize_frame],

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

# Close the window
window.close()
