import os
import time

import sentry_sdk
import pandas as pd

from paybyphone_api import login
from paybyphone_api.park import park
from cloud_storage import read_file
from secret_manager import get_secret
from mail import email

SECRET_MANAGER_PROJECT_ID: str = os.getenv('SECRET_MANAGER_PROJECT_ID')
BUCKET_NAME: str = os.getenv('BUCKET_NAME', 'paybyphone')
LICENCE_PLATES_FILE: str = os.getenv('LICENCE_PLATES_FILE', 'licence_plates.csv')

sentry_sdk.init(
    dsn=get_secret(SECRET_MANAGER_PROJECT_ID, 'sentry_dsn'),
    traces_sample_rate=1.0,
)


def get_licence_plates() -> list:
    """
    Get the licence plates
    :return: The licence plates
    """
    df: pd.DataFrame = read_file(bucket_name=BUCKET_NAME, file_name=LICENCE_PLATES_FILE)
    return df['licence_plate'].to_list()


def main(event, context):
    """
    Main function
    :param event: The event
    :param context: The context
    :return: None
    """
    licence_plates: list = get_licence_plates()
    phone_number: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'paybyphone_phone_number')
    password: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'paybyphone_password')
    parking_account: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'paybyphone_parking_account')
    bearer_token: str = login(phone_number=phone_number, password=password)
    plates_parked: dict = {}
    for licence_plate in licence_plates:
        print(f"Parking {licence_plate}", flush=True)
        if park(parking_account, bearer_token, licence_plate):
            print(f"Successfully parked {licence_plate}", flush=True)
            plates_parked[licence_plate] = True
        else:
            print(f"Failed to park {licence_plate}", flush=True)
            plates_parked[licence_plate] = False
        time.sleep(10)


    email_body: str = f"{'All plates were parked successfully' if all(plates_parked.values()) else 'Some plates failed to park'}<br><br>"
    email_body += "<br>".join(
        [
            f"{licence_plate} - {'Parked successfully' if plates_parked[licence_plate] else 'Failed to park'}"
            for licence_plate in plates_parked.keys()
        ]
    )

    email(
        to=get_secret(SECRET_MANAGER_PROJECT_ID, 'email_recipient'),
        subject='PayByPhone Parking',
        body=email_body
    )
