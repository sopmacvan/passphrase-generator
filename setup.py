from pysqlitecipher import sqlitewrapper
import PySimpleGUI as sg
import hashlib


def create_master_password():
    """
    Ask for password input, and return it hashed to be used later as a master password.
    """

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


def setup():
    """
    1. Create and save a hashed master password in user folder.
    2. Create database and use the hashed master password to protect it.
    3. Create accounts table.
    :return:
    """
    passwords = sg.UserSettings(filename='user/login.json', autosave=True)
    # create master password
    login_password_hash = create_master_password()
    # save master password
    passwords['login'] = login_password_hash

    # create db and protect w/ hashed master password
    obj = sqlitewrapper.SqliteCipher(dataBasePath="user/test.db", checkSameThread=False, password=login_password_hash)

    # create accounts table
    col_list = [["username", "TEXT"], ["password", "TEXT"], ]
    obj.createTable('accounts', col_list, makeSecure=False, commit=True)


# # insert data
# obj.insertIntoTable('accounts', ['john', '123'], commit=True)
#
# # read data
# data = obj.getDataFromTable('accounts', raiseConversionError=True, omitID=False)
# print(data)

if __name__ == '__main__':
    setup()
