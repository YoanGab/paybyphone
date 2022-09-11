import requests
from configparser import ConfigParser
import os

config: ConfigParser = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))


def get_active_parkings(bearer_token: str) -> list:
    """
    Get the active parkings
    :param bearer_token: The bearer token
    :return: The active parkings
    """
    PARKING_ACCOUNT: str = config['PAY_BY_PHONE']['PARKING_ACCOUNT']
    url: str = f"https://consumer.paybyphoneapis.com/parking/accounts/{PARKING_ACCOUNT}/sessions?periodType=Current"

    headers: dict = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response: requests.Response = requests.request("GET", url, headers=headers)
    return response.json()


def has_active_parking(bearer_token: str, license_plate: str) -> bool:
    """
    Check if the vehicle has an active parking
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :return: True if the vehicle has an active parking, False otherwise
    """
    active_parkings: list = get_active_parkings(bearer_token)
    license_plates: list = [parking['vehicle']['licensePlate'] for parking in active_parkings]
    return license_plate in license_plates
