from paybyphone_api import get_quote_id, add_vehicle, is_vehicle_registered, has_active_parking
import requests
import json
from configparser import ConfigParser
import os
from datetime import datetime
import time

config: ConfigParser = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))


def park(parking_account: str, bearer_token: str, license_plate: str, ) -> bool:
    """
    Park the vehicle
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :return: True if the vehicle is parked, False otherwise
    """

    url: str = f"https://consumer.paybyphoneapis.com/parking/accounts/{parking_account}/sessions/"
    if not is_vehicle_registered(bearer_token, license_plate):
        time.sleep(3)
        add_vehicle(bearer_token, license_plate)
        time.sleep(2)

    if has_active_parking(parking_account, bearer_token, license_plate):
        return False

    time.sleep(2)
    quote_id: str = get_quote_id(parking_account, bearer_token, license_plate)
    time.sleep(2)
    payload: str = json.dumps({
        "expireTime": None,
        "duration": {
            "quantity": "1",
            "timeUnit": "days"
        },
        "licensePlate": license_plate,
        "locationId": "75100",
        "rateOptionId": "75100",
        "startTime": (datetime.utcnow().isoformat() + "Z").split(".")[0],
        "quoteId": quote_id,
        "parkingAccountId": parking_account,
    })

    headers: dict = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    response: requests.Response = requests.request("POST", url, headers=headers, data=payload)
    return 200 <= response.status_code < 300
