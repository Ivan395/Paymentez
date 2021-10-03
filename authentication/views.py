import base64
import os
import time
import hashlib
from base64 import b64encode


class TokenPaymentez:
    _UNIXTIMESTAMP = 0

    @classmethod
    def get_token_authentication_paymentez(cls):
        server_application_code: str = os.environ.get('APPLICATION_CODE')
        server_app_key: str = os.environ.get('UNIQ_TOKEN')
        unix_timestamp: str = str(int(time.time()))
        if cls._UNIXTIMESTAMP - int(unix_timestamp) > 15:
            cls._UNIXTIMESTAMP = int(unix_timestamp)
        else:
            unix_timestamp = str(cls._UNIXTIMESTAMP)
        uniq_token_string: str = server_app_key + unix_timestamp
        uniq_token_hash: str = hashlib.sha256(uniq_token_string.encode('utf-8')).hexdigest()
        auth_token = b64encode(f'{server_application_code};{unix_timestamp};{uniq_token_hash}'.encode())
        return auth_token.decode('utf-8')
