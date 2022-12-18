import PySimpleGUI as sg
import hashlib


def password_matches(password, a_hash):
    # check if input password matches master password
    if password is None:
        quit()
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()

    return password_hash == a_hash


def authenticate():
    passwords = sg.UserSettings(filename='user/login.json', autosave=True)
    # get master password
    login_password_hash = passwords.get('login')

    if login_password_hash is None:
        sg.popup('No master password yet. Please run setup.py')
        quit()

    while True:
        # login
        password = sg.popup_get_text('Enter your Master Password', password_char='*')
        if password_matches(password, login_password_hash):
            print('Login SUCCESSFUL')
            break
        else:
            print('Login FAILED')
            sg.popup_error('Login FAILED!!')
