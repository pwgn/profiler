import datetime
import sqlite3
from bson import json_util
import json

PROFILE_STATUS_READY = 'READY'
PROFILE_STATUS_PROCESSING = 'PROCESSING'
PROFILE_STATUS_DELETED = 'DELETED'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class ProfileStore:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self._init_db(self.conn)

    def get(self, key):
        p = self.conn.execute("SELECT * FROM profile WHERE profile_id = '{profile_id}';".format(profile_id=key))
        profile = self._dbo_to_profile(p.fetchone())
        return profile

    def set(self, key, value):
        profile_id = key
        status = value['status']
        profile_path = None if 'profile_path' not in value else value['profile_path']
        timestamp = value['timestamp']
        self.conn.execute(f'''INSERT OR REPLACE INTO profile (
                                profile_id,
                                status,
                                profile_path,
                                timestamp)
                            VALUES ('{profile_id}', '{status}', '{profile_path}', '{timestamp}');
                    ''')
        self.conn.commit()

    def delete_by(self, timestamp_threshold):
        timestamp_format = timestamp_threshold.strftime(DATETIME_FORMAT)
        p = self.conn.execute(f"SELECT profile_id FROM profile WHERE timestamp < '{timestamp_format}' AND status != 'DELETED';")
        self.conn.execute(f'''UPDATE profile
                                        SET status = '{PROFILE_STATUS_DELETED}'
                                        WHERE timestamp < '{timestamp_format}'
                                        AND status != '{PROFILE_STATUS_DELETED}';
                                    ''')
        self.conn.commit()
        deleted_profile_ids = [profile_id for profile_id, in p.fetchall()]
        return deleted_profile_ids

    def _dbo_to_profile(self, values):
        profile_keys = ['profile_id', 'status', 'profile_path', 'timestamp']
        profile = dict(zip(profile_keys, values))
        profile['timestamp'] = datetime.datetime.strptime(profile['timestamp'], DATETIME_FORMAT)
        return profile

    def _init_db(self, conn):
        conn.execute('''CREATE TABLE IF NOT EXISTS profile (
                            profile_id VARCHAR(255) PRIMARY KEY,
                            status VARCHAR(255),
                            profile_path TEXT,
                            timestamp DATETIME
                    );''')
        conn.commit()
