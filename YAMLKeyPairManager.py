import os
from cryptography.fernet import Fernet
import yaml

class YAMLKeyPairManager:
    def __init__(self, base_dir, encryption_key_path):
        self.base_dir = os.path.expanduser(base_dir)
        self.encryption_key = self._load_or_generate_key(encryption_key_path)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def _load_or_generate_key(self, key_path):
        if not os.path.exists(key_path):
            key = Fernet.generate_key()
            with open(key_path, 'wb') as file:
                file.write(key)
        with open(key_path, 'rb') as file:
            return file.read()

    def _get_file_path(self, key_name):
        return os.path.join(self.base_dir, f"{key_name}.yaml.enc")

    def save_key_pair(self, key_name, value):
        cipher = Fernet(self.encryption_key)
        data = {key_name: value}
        encrypted_data = cipher.encrypt(yaml.dump(data).encode())
        with open(self._get_file_path(key_name), 'wb') as file:
            file.write(encrypted_data)

    def retrieve_key_pair(self, key_name):
        file_path = self._get_file_path(key_name)
        if not os.path.exists(file_path):
            return None
        cipher = Fernet(self.encryption_key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        data = yaml.safe_load(decrypted_data.decode())
        return data.get(key_name)

    def delete_key_pair(self, key_name):
        file_path = self._get_file_path(key_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def update_key_pair(self, key_name, new_value):
        # Updating a value is essentially the same as saving it,
        # since each key-value pair is stored in its own file.
        self.save_key_pair(key_name, new_value)
        
# Example usage
# if __name__ == "__main__":
    # base_dir = "/elt/.syskey/kpmgr"
    # encryption_key_path = "/elt/.syskey/encryption_key.key"

    # manager = YAMLKeyPairManager(base_dir, encryption_key_path)
    # #manager.save_key_pair("test", "vltest")  # Save initial value
    
    # print(manager.retrieve_key_pair("test"))
