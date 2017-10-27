
import requests
import hashlib
import json
import logging
import mysql.connector

from mysql.connector import errorcode

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.ERROR)
log = logging.getLogger(__name__)


class CatServerExporter(object):

    USE_LOCAL = True
    TABLE = None
    TABLE_SCHEMA = None

    def __init__(self):

        try:
            from settings import USE_LOCAL_DB
            self.USE_LOCAL = USE_LOCAL_DB
        except ImportError:
            log.error('Could not find USE_LOCAL_DB setting. Attempting to use remote.')
            self.USE_LOCAL = False

        if self.USE_LOCAL:
            try:
                from settings import LOCAL_DB_CONFIG
                self.TABLE = LOCAL_DB_CONFIG.get('table', 'scraped_data')
                self.TABLE_SCHEMA = LOCAL_DB_CONFIG.get('table_schema', [])
            except ImportError:
                log.error('Could not find USE_LOCAL_DB setting. Using default \'scraped_data\' MySQL Table')

            self.check_local_db()

    def mysql_query(self, query, params, commit=True):

        results = None

        try:
            from settings import LOCAL_DB_CONFIG

            conn = mysql.connector.connect(**LOCAL_DB_CONFIG.get('mysql', {}))
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = list(cursor)

            if commit:
                conn.commit()

            conn.close()
            cursor.close()

        except ImportError:
            log.error('Could not find LOCAL_DB_CONFIG setting. Check settings file.')
            raise
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.error("MySQL Error: Wrong username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log.error("MySQL Error: Database does not exist")
            else:
                log.error(err)
            raise
        else:
            conn.close()
            cursor.close()

        return results

    def check_local_db(self):
        """
        Checks to see if the database and tables are created
        :return:
        """
        query = """SELECT * FROM %s""" % self.TABLE
        results = self.mysql_query(query, ())

        if results is None:
            raise Exception("Database not configured correctly. Could not select from table \'%s\'" % self.TABLE)

    def export(self, json_textsample):
        line = json.dumps(json_textsample)
        line_hash = hashlib.sha256(line).hexdigest()

        # positions: [<link:str>, <filter-score:int>, <pw-list:list>, <metrics:dict>]
        text_link = json_textsample[0]
        text_score = json_textsample[1]
        poss_pws = json_textsample[2]

        metrics = json_textsample[3]
        basic_freqs = metrics.get('basic_frequencies', {})
        raw_text_hash = metrics.get('hash', None)

        data = {
            'category': None,
            'raw_values': line,
            'raw_values_hash': line_hash,
            'link': text_link,
            'filter_score': text_score,
            'basic_frequencies': json.dumps(basic_freqs),
            'raw_text_hash': raw_text_hash,
        }

        if self.USE_LOCAL:
            self.export_to_local(data)
        else:
            CatServerExporter.export_to_remote(data)

    def export_to_local(self, data):

        print(data)

        query = (
            """INSERT INTO scraped_data """
            """(category, raw_values, raw_values_hash, link, filter_score, basic_frequencies, raw_text_hash) """
            """VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        )

        tuple_data = (
            data.get('category'),
            data.get('raw_values'),
            data.get('raw_values_hash'),
            data.get('link'),
            data.get('filter_score'),
            data.get('basic_frequencies'),
            data.get('raw_text_hash'),
        )

        results = self.mysql_query(query, tuple_data)

    @staticmethod
    def export_to_remote(data):
        try:
            from settings import CAT_SERVER_CONFIG
            headers = {
                'Authorization': 'Token %s' % CAT_SERVER_CONFIG.get('token', ''),
                'Content-Type': 'application/json'
            }

            url = '%s/%s/' % (CAT_SERVER_CONFIG.get('address', ''), CAT_SERVER_CONFIG.get('api_endpoint', ''))

            r = requests.post(url, json=data, headers=headers)

            if r.status_code != 201:
                log.error('Could not create instance -- received HTTP status code other than 201.')
                raise IOError('Could not create instance')

        except ImportError:
            log.error('Could not find CAT_SERVER_CONFIG setting. Check settings file.')
        except IOError:
            log.error('Unexpeted IO error: Could not export data to Categorization Server.')

