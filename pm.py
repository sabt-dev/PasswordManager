from cryptography.fernet import Fernet, InvalidToken
from tkinter.messagebox import showerror


class passwordManager:

    def __init__(self):
        self.key = None
        self.pwd_file = None
        self.pwd_dict: dict = {}
        self.array_checker: set[tuple[str, str, str]] = set()
        self.checkKeyValidility: bool = False

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
        self.pwd_dict = {}
        self.array_checker = set()
        with open(self.pwd_file, 'w'):
            pass

        if initial_values is not None:
            for primeKey, subKey in initial_values.items():
                for key, value in subKey.items():
                    self.add_password(primeKey, key, value)

    def load_passwordFile(self, path):
        self.pwd_file = path
        self.pwd_dict = {}
        self.array_checker = set()
        self.checkKeyValidility = False

        try:
            with open(path, 'r') as f:
                for line in f:
                    try:
                        site, email, encrypted_pwd = line.rstrip('\n').split(':', 2)
                        decrypted_pass = Fernet(self.key).decrypt(encrypted_pwd.encode()).decode()
                        self.pwd_dict.setdefault(site, {})[email] = decrypted_pass
                        self.array_checker.add((site, email, decrypted_pass))
                    except ValueError:
                        continue
                self.checkKeyValidility = True
        except FileNotFoundError:
            pass
        except TypeError:
            showerror('Error', '!!!the key is required first!!!')
        except InvalidToken:
            self.checkKeyValidility = False
            showerror('Error', '!!!Invalid key!!!')

    def add_password(self, site, email, password):
        entry = (site, email, password)
        self.pwd_dict.setdefault(site, {})[email] = password

        if self.pwd_file is not None:
            if self.key is None:
                raise ValueError('A key must be loaded before adding passwords')
            with open(self.pwd_file, 'a+') as f:
                if entry not in self.array_checker:
                    encrypted = Fernet(self.key).encrypt(password.encode())
                    f.write(site + ':' + email + ':' + encrypted.decode() + '\n')
                    self.array_checker.add(entry)

        if self.pwd_file is not None:
            self.load_passwordFile(self.pwd_file)

    def get_password(self, site) -> list:
        for primeKey, subKey in self.pwd_dict.items():
            for key, value in subKey.items():
                if primeKey == site:
                    return [site, key, value]

    def getAllSites(self) -> list:
        # passwordManager.load_passwordFile(self, self.pwd_file)
        return list(self.pwd_dict)

    def delete_site(self, targetedSite):
        if self.pwd_file is None:
            return

        new_list: list[str] = []

        with open(self.pwd_file, 'r') as f:
            lines: list = f.readlines()
            for line in lines:
                site, _, _ = line.rstrip('\n').split(':', 2)
                if targetedSite != site:
                    new_list.append(line)

        with open(self.pwd_file, 'w') as f:
            for line in new_list:
                f.write(line)

        self.load_passwordFile(self.pwd_file)
