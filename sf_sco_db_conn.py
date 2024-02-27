import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

user = os.environ.get('SF_Connection_proc_acct')
#print(user)

key_path = os.environ.get('SF_Connection_PRIVATE_KEY_PATH')
#print(path)


def get_snowflake_conn(database,schema):
    with open(key_path, "rb") as key:
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
        user=user,
        account='videotron-freedommobile',
        private_key=pkb,
        #warehouse="ANALYST_WH",
        database=database,
        schema=schema
        
    )
    return ctx



# with open(key_path, "rb") as key:
    # p_key= serialization.load_pem_private_key(
        # key.read(),
        # password=os.environ['SF_Connection_PRIVATE_KEY_PASSPHRASE'].encode(),
        # backend=default_backend()
    # )

# pkb = p_key.private_bytes(
    # encoding=serialization.Encoding.DER,
    # format=serialization.PrivateFormat.PKCS8,
    # encryption_algorithm=serialization.NoEncryption())

# ctx = snowflake.connector.connect(
    # user=user,
    # account='videotron-freedommobile',
    # private_key=pkb,
    # #warehouse="ANALYST_WH",
    # database="INT_SCO_DB",
    # schema="LANDING"
    
# )



# # # Use `ctx` as needed...
# LND_cs = get_snowflake_conn('INT_SCO_DB','LANDING').cursor()
# #LND_cs.execute("SELECT count(1) FROM INT_SCO_DB.LANDING.L0_WAREHOUSE_INVENTORY_EBS_DAILY;")
# LND_cs.execute("SELECT CURRENT_SCHEMA();")
# result = LND_cs.fetch_pandas_all()
# print(result)