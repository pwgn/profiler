from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from profiler import ProfileStore
from typing import List
import logging
import asyncio
import datetime

app = FastAPI()
logger = logging.getLogger(__name__)
profile_store = ProfileStore()

@app.get("/", response_class = HTMLResponse)
def index():
    f = open(f'frontend/index.html', "r")
    return f.read()

@app.get("/profile/{profile_id}", response_class = HTMLResponse)
async def read_results(profile_id: str):
    profile_file = profile_store.get_profile(profile_id)
    return profile_file.read()

@app.post("/profile/")
async def profile_file(files: List[UploadFile]):
    profile_id = await profile_store.create_profile(files[0])
    return {'profile_id': profile_id}

@app.on_event('startup')
async def schedule_profile_cleaner():
    async def run():
        while True:
            profile_store.clean_profiles(datetime.datetime.now())
            print('cleaning profiles')
            await asyncio.sleep(5)

    loop = asyncio.get_event_loop()
    loop.create_task(run())