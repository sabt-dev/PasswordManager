import cryptography.fernet
from cryptography.fernet import Fernet
from tkinter.messagebox import *


class passwordManager:

    def __init__(self):
        self.key = None
        self.pwd_file = None
        self.pwd_dict: dict = {}
        self.array_checker: set = set()
        self.checkKeyValidility: bool = True

    def create_key(self, path):
        try:
            self.key = Fernet.generate_key()
            with open(path, 'wb') as f:
                f.write(self.key)
        except FileNotFoundError:
            pass

    def load_key(self, path):
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
        except FileNotFoundError:
            pass

    def create_passwordFile(self, path, initial_values: dict = None):
        self.pwd_file = path
        with open(self.pwd_file, 'w'):
            pass

        if initial_values is not None:
            for primeKey, subKey in initial_values.items():
                for key, value in subKey.items():
                    self.add_password(primeKey, key, value)

    def load_passwordFile(self, path):
        self.pwd_file = path
        self.pwd_dict = {}

        try:
            with open(path, 'r') as f:
                for line in f:
                    try:
                        site, email, encrypted_pwd = line.split(':')
                        decryptedPass = Fernet(self.key).decrypt(encrypted_pwd.encode()).decode()
                        self.pwd_dict[site] = {email: decryptedPass}
                        self.array_checker = site, email, decryptedPass
                    except ValueError:
                        pass
                # prints the decrypted dictionary, needed to be removed when done!!!
                self.checkKeyValidility = True
                print(self.pwd_dict)
                print(self.array_checker)
        except FileNotFoundError:
            pass
        except TypeError:
            showerror('Error', '!!!the key is required first!!!')
        except cryptography.fernet.InvalidToken:
            self.checkKeyValidility = False
            showerror('Error', '!!!Invalid key!!!')

    def add_password(self, site, email, password):
        self.pwd_dict[site] = {email: password}
        # self.array_checker = site, email, password

        if self.pwd_file is not None:
            with open(self.pwd_file, 'a+') as f:
                if (site not in self.array_checker) or \
                        (email not in self.array_checker) or (password not in self.array_checker):
                    encrypted = Fernet(self.key).encrypt(password.encode())
                    f.write(site + ':' + email + ':' + encrypted.decode() + '\n')

        # to check there's no repetitive same line when pressing submit button multiple times
        # recalling the function "load_passwordFile" from a class "passwordManager"
        passwordManager.load_passwordFile(self, self.pwd_file)

    def get_password(self, site) -> list:
        for primeKey, subKey in self.pwd_dict.items():
            for key, value in subKey.items():
                if primeKey == site:
                    return [site, key, value]

    def getAllSites(self) -> list:
        # passwordManager.load_passwordFile(self, self.pwd_file)
        return list(self.pwd_dict)

    def delete_site(self, targetedSite):
        newList: list = []

        with open(self.pwd_file, 'r') as f:
            lines: list = f.readlines()
            for line in lines:
                site, email, encrypted_pwd = line.split(':')
                if targetedSite != site:
                    newList.append(line)

        with open(self.pwd_file, 'w') as f:
            for line in newList:
                f.write(line)

        passwordManager.load_passwordFile(self, self.pwd_file)
