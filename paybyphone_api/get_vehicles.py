import requests


def get_vehicles(bearer_token: str) -> list:
    """
    Get the vehicles
    :param bearer_token: The bearer token
    :return: The vehicles
    """
    url: str = "https://consumer.paybyphoneapis.com/identity/profileservice/v1/members/vehicles/paybyphone"

    headers: dict = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response: requests.Response = requests.request("GET", url, headers=headers)
    return response.json()


def get_all_license_plates(bearer_token: str) -> list:
    """
    Get all the license plates
    :param bearer_token: The bearer token
    :return: The license plates
    """
    vehicles: list = get_vehicles(bearer_token)
    return [vehicle['licensePlate'] for vehicle in vehicles]


def is_vehicle_registered(bearer_token: str, license_plate: str) -> bool:
    """
    Check if the vehicle is registered
    :param bearer_token: The bearer token
    :param license_plate: The license plate of the vehicle
    :return: True if the vehicle is registered, False otherwise
    """
    license_plates: list = get_all_license_plates(bearer_token)
    return license_plate in license_plates
