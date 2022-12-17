import PySimpleGUI as sg
import hashlib

"""
    Create a secure login for your scripts without having to include your password 
    in the program.  Create an SHA1 hash code for your password using the GUI. Paste into variable in final program
    1. Choose a password
    2. Generate a hash code for your chosen password by running program and entering 'gui' as the password
    3. Type password into the GUI
    4. Copy and paste hash code from GUI into variable named login_password_hash
    5. Run program again and test your login!
    6. Are you paying attention? The first person that can post an issue on GitHub with the
       matching password to the hash code in this example gets a $5 PayPal payment
"""


def create_master_password():
    # create master password
    def generate_hash(password):
        # generate and return a hash for the password
        password_utf = password.encode('utf-8')
        sha1hash = hashlib.sha1()
        sha1hash.update(password_utf)
        password_hash = sha1hash.hexdigest()

        return password_hash

    def length_greater_than_6(password):
        # check if password length is greater than 7
        return len(password) > 7

    while True:
        password = sg.popup_get_text('Setup: Create your Master Password')
        if password is None:
            quit()
        if not length_greater_than_6(password):
            sg.popup('Password length must be 8 or greater.')
            continue

        login_password_hash = generate_hash(password)
        return login_password_hash


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
    passwords = sg.UserSettings(filename='user/passwords.json', autosave=True)
    # get master password
    login_password_hash = passwords.get('login')

    if login_password_hash is None:
        # create master password
        login_password_hash = create_master_password()
        # save master password
        passwords['login'] = login_password_hash

    while True:
        # login
        password = sg.popup_get_text('Enter your Master Password', password_char='*')
        if password_matches(password, login_password_hash):
            print('Login SUCCESSFUL')
            break
        else:
            print('Login FAILED')
            sg.popup_error('Login FAILED!!')
