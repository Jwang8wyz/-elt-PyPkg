import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
import sys


sys.path.append('/elt/PyPkg/')
from YAMLKeyPairManager import YAMLKeyPairManager
manager = YAMLKeyPairManager('/elt/.syskey/kpmgr', '/elt/.syskey/encryption_key.key')
user=manager.retrieve_key_pair("SF_Connection_proc_acct")
key_path=manager.retrieve_key_pair("SF_Connection_PRIVATE_KEY_PATH")

# user = os.environ['SF_Connection_proc_acct']
# #print(user)

# key_path = os.environ['SF_Connection_PRIVATE_KEY_PATH']
# #print(key_path)

def get_snowflake_conn(database,schema):
    with open(key_path, "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            #password=os.environ['SF_Connection_PRIVATE_KEY_PASSPHRASE'].encode(),
            password=manager.retrieve_key_pair("SF_Connection_PRIVATE_KEY_PASSPHRASE").encode(),
            backend=default_backend()
        )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    ctx = snowflake.connector.connect(
        user=user,
        account='videotron-freedommobile',
        private_key=pkb,
        #warehouse="ANALYST_WH",
        database=database,
        schema=schema
        
    )
    return ctx


