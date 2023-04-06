from datetime import datetime
from pathlib import Path
from ydata_profiling import ProfileReport
import os
import pandas as pd
import uuid
from sqlitestore import SQLite

DEFAULT_PROFILE_RESULT_DIR = 'profile_result_store'
PROFILE_STORE = 'profile_store.db'

PROFILE_STATUS_READY = 'READY'
PROFILE_STATUS_PROCESSING = 'PROCESSING'

class ProfileStore:
    def __init__(self):
        if not os.path.exists(DEFAULT_PROFILE_RESULT_DIR):
            os.makedirs(DEFAULT_PROFILE_RESULT_DIR)
        self.profiles = SQLite(f'{DEFAULT_PROFILE_RESULT_DIR}/{PROFILE_STORE}')

    async def create_profile(self, input_file):
        profile_id = str(uuid.uuid4())
        timestamp = datetime.now()

        self.profiles.set(profile_id, {
                            'status': PROFILE_STATUS_PROCESSING,
                            'timestamp': timestamp})

        profile_file_path = self._profile_file(profile_id, input_file)

        self.profiles.set(profile_id, {
                            'status': PROFILE_STATUS_READY,
                            'profile_path': profile_file_path,
                            'timestamp': timestamp})

        return profile_id

    def get_profile(self, profile_id):
        profile_result = self.profiles.get(profile_id)

        if profile_result is None:
            return {"error": "Profile not found"}

        profile_file_path = profile_result['profile_path']

        f = open(profile_file_path, "r")
        return f

    def _profile_file(self, profile_id, input_file):
        directory_path = os.path.join('.', f'{DEFAULT_PROFILE_RESULT_DIR}/{profile_id}')
        os.makedirs(directory_path)

        file_path = os.path.join(directory_path, input_file.filename)
        with open(file_path, 'wb') as f:
            f.write(input_file.file.read())

        profile_file_path = profile(file_path, directory_path)

        return profile_file_path

def profile(inputfile: str, outputdir: str = None):
    print(f'profiling:{inputfile}')

    result_dir = outputdir if outputdir is not None else DEFAULT_PROFILE_RESULT_DIR

    df_input = pd.read_csv(inputfile, engine='python', sep = None)
    filename = os.path.basename(inputfile)
    profile = ProfileReport(df_input, title=filename)

    result_location = f'{result_dir}/{Path(filename).stem}.html'
    profile.to_file(result_location)

    print(f'profiling result location:{result_location}')

    return result_location