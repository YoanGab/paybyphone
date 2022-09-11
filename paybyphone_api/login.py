import requests
import os
from configparser import ConfigParser

config: ConfigParser = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))


def login() -> str:
    """
    Login to PayByPhone and return the bearer token
    :return: The bearer token
    """

    url: str = "https://auth.paybyphoneapis.com/token"
    payload: str = f"grant_type=password&username=%2B{config['PAY_BY_PHONE']['PHONE_NUMBER']}&password={config['PAY_BY_PHONE']['PASSWORD']}&client_id=paybyphone_web"
    headers: dict = {
        'X-Pbp-ClientType': 'WebApp',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'auth.paybyphoneapis.com',
        'Origin': 'https://m2.paybyphone.fr',
        'Referer': 'https://m2.paybyphone.fr/'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["access_token"]
