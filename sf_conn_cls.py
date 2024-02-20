import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, dsa
from cryptography.hazmat.primitives import serialization

class VLFMSnowflakeConnection:
    def __init__(self, user, account, private_key_path_env_var, private_key_passphrase_env_var, database, schema):
        self.user = user
        self.account = account
        self.private_key_path = os.environ.get(private_key_path_env_var)
        self.private_key_passphrase_env_var = private_key_passphrase_env_var
        self.database = database
        self.schema = schema
        self.conn = None

    def _load_private_key(self):
        with open(self.private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=os.environ[self.private_key_passphrase_env_var].encode(),
                backend=default_backend()
            )
        return private_key

    def _get_private_key_bytes(self):
        private_key = self._load_private_key()
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
        return private_key_bytes

    def connect(self):
        if self.conn is None:
            private_key_bytes = self._get_private_key_bytes()
            self.conn = snowflake.connector.connect(
                user=self.user,
                account=self.account,
                private_key=private_key_bytes,
                database=self.database,
                schema=self.schema
            )
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None