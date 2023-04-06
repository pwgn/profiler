import datetime
import sqlite3
from bson import json_util
import json

class SQLite:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self._init_db(self.conn)

    def get(self, key):
        p = self.conn.execute("SELECT * FROM profile;")
        print(p.fetchall())

        p = self.conn.execute("SELECT * FROM profile WHERE profile_id = '{profile_id}';".format(profile_id=key))
        profile = self._dbo_to_profile(p.fetchone())
        return profile

    def set(self, key, value):
        profile_id = key
        status = value['status']
        profile_path = None if 'profile_path' not in value else value['profile_path']
        timestamp = value['timestamp']
        self.conn.execute('''INSERT OR REPLACE INTO profile (
                                profile_id,
                                status,
                                profile_path,
                                timestamp)
                            VALUES ('{profile_id}', '{status}', '{profile_path}', '{timestamp}');
                    '''.format(profile_id=profile_id, status=status, profile_path=profile_path, timestamp=timestamp))
        self.conn.commit()

    def _dbo_to_profile(self, values):
        profile_keys = ['profile_id', 'status', 'profile_path', 'timestamp']
        profile = dict(zip(profile_keys, values))
        profile['timestamp'] = datetime.datetime.strptime(profile['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        return profile

    def _init_db(self, conn):
        conn.execute('''CREATE TABLE IF NOT EXISTS profile (
                            profile_id VARCHAR(255) PRIMARY KEY,
                            status VARCHAR(255),
                            profile_path TEXT,
                            timestamp DATETIME
                    );''')
        conn.commit()
