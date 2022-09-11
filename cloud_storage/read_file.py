from typing import Optional

import pandas as pd
from google.cloud import storage


def read_file(bucket_name: str, file_name: str) -> Optional[pd.DataFrame]:
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    if blob.exists():
        df = pd.read_csv(f'gs://{bucket_name}/{file_name}', sep=';')
        return df
    return None
