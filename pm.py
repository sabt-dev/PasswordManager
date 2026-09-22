import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet, InvalidToken
from tkinter.messagebox import showerror


class passwordManager:

    _MASTER_KEY_HEADER = b'PMK1'
    _SALT_LENGTH = 16
    _VERIFIER = b'SecureVault master key verifier'
    _PBKDF2_ITERATIONS = 600_000

    def __init__(self):
        self.key = None
        self.pwd_file = None
        self.pwd_dict: dict = {}
        self.array_checker: set[tuple[str, str, str]] = set()
        self.checkKeyValidility: bool = False

    def create_key(self, path, master_password):
        try:
            salt = os.urandom(self._SALT_LENGTH)
            self.key = self._derive_key(master_password, salt)
            with open(path, 'wb') as f:
                verifier = hmac.new(self.key, self._VERIFIER, hashlib.sha256).digest()
                f.write(self._MASTER_KEY_HEADER + salt + verifier)
        except FileNotFoundError:
            pass

    def load_key(self, path, master_password=None):
        try:
            with open(path, 'rb') as f:
                key_data = f.read()

            if key_data.startswith(self._MASTER_KEY_HEADER):
                key_payload = key_data[len(self._MASTER_KEY_HEADER):]
                if not master_password or len(key_payload) != self._SALT_LENGTH + hashlib.sha256().digest_size:
                    raise ValueError('A master password is required')
                salt = key_payload[:self._SALT_LENGTH]
                expected_verifier = key_payload[self._SALT_LENGTH:]
                self.key = self._derive_key(master_password, salt)
                verifier = hmac.new(self.key, self._VERIFIER, hashlib.sha256).digest()
                if not hmac.compare_digest(verifier, expected_verifier):
                    self.key = None
                    raise ValueError('Invalid master password')
            else:
                # Keep existing key files usable during the format transition.
                self.key = key_data
        except FileNotFoundError:
            pass

    @classmethod
    def _derive_key(cls, master_password, salt):
        derived_key = hashlib.pbkdf2_hmac(
            'sha256', master_password.encode('utf-8'), salt, cls._PBKDF2_ITERATIONS, 32)
        return base64.urlsafe_b64encode(derived_key)

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
