# import PySimpleGUI as sg
#
#
#
# def create_vault_window():
#     # Define the window's layout
#     layout = [
#         [sg.Button('Create', key=''),sg.Button('Update', key=''),sg.Button('Delete', key=''),sg.Button('Create', key='')],
#         []
#     ]
#     # UI: Set Window Size & BG Color
#     return sg.Window('Passphrase Generator', layout)
#
#
# def create():
#     window = create_vault_window()
#
#     # Event Loop
#     while True:
#         event, values = window.read()
#         # See if window was closed
#         if event in (sg.WIN_CLOSED, '-EXIT-'):
#             break
#
#     # Close window
#     window.close()
#
#
# if __name__ == '__main__':
#     sg.theme('DarkBlack')
#     create()
