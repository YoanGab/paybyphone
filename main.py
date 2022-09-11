import time

import sentry_sdk
import pandas as pd
from configparser import ConfigParser

from paybyphone_api import login
from paybyphone_api.park import park

config: ConfigParser = ConfigParser()
config.read('config.ini')

sentry_sdk.init(
    dsn=config['SENTRY']['DSN'],
    traces_sample_rate=1.0,
)


def get_licence_plates() -> list:
    """
    Get the licence plates
    :return: The licence plates
    """
    df: pd.DataFrame = pd.read_csv('licence_plates.csv')
    return df['licence_plate'].tolist()


def main() -> None:
    """
    Main function
    :return: None
    """
    licence_plates: list = get_licence_plates()
    bearer_token: str = login()
    for licence_plate in licence_plates:
        print(f"Parking {licence_plate}", flush=True)
        if park(bearer_token, licence_plate):
            print(f"Successfully parked {licence_plate}", flush=True)
        else:
            print(f"Failed to park {licence_plate}", flush=True)
        time.sleep(10)


if __name__ == '__main__':
    main()
