from datetime import datetime
from pathlib import Path
from ydata_profiling import ProfileReport
import os
import pandas as pd
import uuid
from dictstore import DictStore

DEFAULT_PROFILE_RESULT_DIR = './profile_result_store'
PROFILE_STORE = 'profile_store.json'

PROFILE_STATUS_READY = 'READY'
PROFILE_STATUS_PROCESSING = 'PROCESSING'

class ProfileStore:
    def __init__(self):
        if not os.path.exists(DEFAULT_PROFILE_RESULT_DIR):
            os.makedirs(DEFAULT_PROFILE_RESULT_DIR)
        self.profiles = DictStore(f'{DEFAULT_PROFILE_RESULT_DIR}/{PROFILE_STORE}')

    def create_profile(self, input_file):
        profile_id = str(uuid.uuid4())
        timestamp = datetime.now()

        self.profiles.set(profile_id, {
                            'status': PROFILE_STATUS_PROCESSING,
                            'timestamp': timestamp})

        profile_file_name = self._profile_file(profile_id, input_file)

        self.profiles.set(profile_id, {
                            'status': PROFILE_STATUS_READY,
                            'file_name': profile_file_name,
                            'timestamp': timestamp})

        return profile_id

    def get_profile(self, profile_id):
        profile_result = self.profiles.get(profile_id)

        if profile_result is None:
            return {"error": "Profile not found"}

        file_name = profile_result['file_name']


        f = open(f'{DEFAULT_PROFILE_RESULT_DIR}/{profile_id}/{file_name}.html', "r")
        return f

    def _profile_file(self, profile_id, input_file):
        directory_path = os.path.join('.', f'{DEFAULT_PROFILE_RESULT_DIR}/{profile_id}')
        os.makedirs(directory_path)

        file_path = os.path.join(directory_path, input_file.filename)
        with open(file_path, 'wb') as f:
            f.write(input_file.file.read())

        profile_file_name = profile(file_path, directory_path)

        return profile_file_name

def profile(inputfile: str, outputdir: str = None):
    print(f'profiling:{inputfile}')

    result_dir = outputdir if outputdir is not None else DEFAULT_PROFILE_RESULT_DIR

    df_input = pd.read_csv(inputfile, sep = None)
    filename = os.path.basename(inputfile)
    profile = ProfileReport(df_input, title=filename)

    result_location = f'{result_dir}/{filename}'
    profile.to_file(result_location)

    print(f'profiling result location:{result_location}')

    profile_file_name = Path(result_location).stem
    return profile_file_name