import requests
import os


def get_active_parkings(parking_account: str, bearer_token: str) -> list:
    """
    Get the active parkings
    :param bearer_token: The bearer token
    :return: The active parkings
    """
    url: str = f"https://consumer.paybyphoneapis.com/parking/accounts/{parking_account}/sessions?periodType=Current"

    headers: dict = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response: requests.Response = requests.request("GET", url, headers=headers)
    return response.json()


def has_active_parking(parking_account: str, bearer_token: str, license_plate: str) -> bool:
    """
    Check if the vehicle has an active parking
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :return: True if the vehicle has an active parking, False otherwise
    """
    active_parkings: list = get_active_parkings(parking_account, bearer_token)
    license_plates: list = [parking['vehicle']['licensePlate'] for parking in active_parkings]
    return license_plate in license_plates
