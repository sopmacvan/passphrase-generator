import PySimpleGUI as sg
from pysqlitecipher import sqlitewrapper
import pyperclip


# ---------- CRUD operations ----------#

def create_account(vault):
    layout = [
        [sg.Text('Create new account.')],
        [sg.Text('Name', size=(15, 1)), sg.InputText(key='-NAME-')],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-')],
        [sg.Text('Password', size=(15, 1)), sg.InputText(key='-PASSWORD-')],
        [sg.Submit(button_text='Create', key='-CREATE-'), sg.Cancel(key='-CANCEL-')]
    ]
    window = sg.Window('Create new', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-CANCEL-'):
            break
        if event == '-CREATE-':
            name = values['-NAME-']
            username = values['-USERNAME-']
            password = values['-PASSWORD-']
            vault.insertIntoTable('accounts', [name, username, password], commit=True)
            break

    window.close()


def update_account(id_value, name, username, password, vault):
    layout = [
        [sg.Text('Edit old account.')],
        [sg.Text('Name', size=(15, 1)), sg.InputText(default_text=name, key='-NAME-')],
        [sg.Text('Username', size=(15, 1)), sg.InputText(default_text=username, key='-USERNAME-')],
        [sg.Text('Password', size=(15, 1)), sg.InputText(default_text=password, key='-PASSWORD-')],
        [sg.Submit(button_text='Save', key='-SAVE-'), sg.Cancel(key='-CANCEL-')]
    ]
    window = sg.Window('Edit', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-CANCEL-'):
            break
        if event == '-SAVE-':
            name = values['-NAME-']
            username = values['-USERNAME-']
            password = values['-PASSWORD-']

            # update name, username, and password in database
            vault.updateInTable('accounts', id_value, 'name', name, commit=True, raiseError=True)
            vault.updateInTable('accounts', id_value, 'username', username, commit=True, raiseError=True)
            vault.updateInTable('accounts', id_value, 'password', password, commit=True, raiseError=True)
            break

    window.close()


def delete_account(id_value, vault):
    vault.deleteDataInTable('accounts', id_value, commit=True, raiseError=True, updateId=True)


# ---------- Main window ----------#

def create_vault_window():
    def refresh_table():
        data = vault.getDataFromTable('accounts', raiseConversionError=True, omitID=False)
        table_header = data[0]
        table_rows = data[1]
        window['-TABLE-'].update(values=table_rows)

    def no_row_selected():
        return len(values['-TABLE-']) == 0

    login_pass = '12345678'
    vault = sqlitewrapper.SqliteCipher(dataBasePath="user/vault.db", checkSameThread=False, password=login_pass)
    # read data
    data = vault.getDataFromTable('accounts', raiseConversionError=True, omitID=False)
    table_header = data[0]
    table_rows = data[1]

    # Define the window's layout
    accounts_table = [
        sg.Table(values=table_rows, headings=table_header, auto_size_columns=False,
                 num_rows=10, justification='center', enable_events=True,
                 alternating_row_color='green', select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 key='-TABLE-')]

    layout = [
        [sg.Button('Create', key='-CREATE-'), sg.Button('Edit', key='-EDIT-'), sg.Button('Delete', key='-DELETE-')],
        [accounts_table],
        [sg.Button('Copy Username', key='-COPY USERNAME-'), sg.Button('Copy Password', key='-COPY PASSWORD-')],

    ]
    window = sg.Window('Pass Vault', layout)

    # ---------- EVENT LOOP ----------#
    while True:
        event, values = window.read()
        # See if window was closed
        if event == sg.WIN_CLOSED:
            break

        if event == '-CREATE-':
            create_account(vault)
            refresh_table()

        if event == '-EDIT-':
            if no_row_selected():
                continue
            id_value = values['-TABLE-'][0]

            name = table_rows[id_value][-3]
            username = table_rows[id_value][-2]
            password = table_rows[id_value][-1]
            update_account(id_value, name, username, password, vault)
            refresh_table()

        if event == '-DELETE-':
            if no_row_selected():
                continue

            id_value = values['-TABLE-'][0]

            delete_account(id_value, vault)
            refresh_table()

        if event == '-COPY USERNAME-':
            if no_row_selected():
                continue

            id_value = values['-TABLE-'][0]

            username = table_rows[id_value][-2]
            pyperclip.copy(username)

        if event == '-COPY PASSWORD-':
            if no_row_selected():
                continue

            id_value = values['-TABLE-'][0]

            password = table_rows[id_value][-1]
            pyperclip.copy(password)
    # Close window
    window.close()


if __name__ == '__main__':
    sg.theme('DarkBlack')
    create_vault_window()
