import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

def get_snowflake_conn():
    with open("/home/jwang/10_200_52_21__rsa.p8", "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            password=os.environ['SF_Connection_PRIVATE_KEY_PASSPHRASE'].encode(),
            backend=default_backend()
        )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    ctx = snowflake.connector.connect(
        user='proc_int_sco_national_retail_tospcetlapn01',
        account='videotron-freedommobile',
        private_key=pkb,
        #warehouse="ANALYST_WH",
        database="INT_SCO_DB",
        schema="LANDING"
        
    )
    return ctx