
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

USE_LOCAL_DB = False
LOCAL_DB_CONFIG = {
    'mysql': {
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'database': 'pbscraper',
    },
    'table': 'scraped_data',
    'table_schema': [
        'category',
        'raw_values',
        'raw_values_hash',
        'link',
        'filter_score',
        'basic_frequencies',
        'raw_text_hash',
    ]
}

CAT_SERVER_CONFIG = {
    'token': '2c916dcb4f4c0ec941caff9c01f09968fd28d9a5',
    'address': 'http://127.0.0.1:8000',
    'api_endpoint': 'textsamples',
}
