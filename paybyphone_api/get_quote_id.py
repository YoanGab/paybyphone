import requests
from configparser import ConfigParser
import os

config: ConfigParser = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))


def get_quote_id(bearer_token: str, license_plate: str) -> str:
    """
    Get the quote id
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :return: The quote id
    """
    PARKING_ACCOUNT: str = config['PAY_BY_PHONE']['PARKING_ACCOUNT']
    url: str = f"https://consumer.paybyphoneapis.com/parking/accounts/{PARKING_ACCOUNT}/quote?locationId=75100&licensePlate={license_plate}&stall=&rateOptionId=75100&durationTimeUnit=Days&durationQuantity=1&isParkUntil=false&expireTime=&parkingAccountId={PARKING_ACCOUNT} "

    headers: dict = {'Authorization': f'Bearer {bearer_token}'}

    response: requests.Response = requests.request("GET", url, headers=headers)
    return response.json()['quoteId']
