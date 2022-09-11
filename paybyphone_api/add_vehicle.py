import requests
import json


def add_vehicle(bearer_token: str, license_plate: str, vehicle_type: str = "car") -> bool:
    """
    Add a vehicle to the account
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :param vehicle_type: The type of the vehicle
    :return: True if the vehicle has been added, False otherwise
    """

    url: str = "https://consumer.paybyphoneapis.com/identity/profileservice/v1/members/vehicles/paybyphone"

    payload: str = json.dumps({
        "licensePlate": license_plate,
        "jurisdiction": "",
        "country": "FR",
        "type": vehicle_type
    })
    headers: dict = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    response: requests.Response = requests.request("POST", url, headers=headers, data=payload)
    return 200 <= response.status_code < 300
