from fastapi import FastAPI, UploadFile, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from profiler import Profiler
from typing import List
import json
import logging
import asyncio
import datetime

app = FastAPI()
logger = logging.getLogger(__name__)
profile_store = Profiler()

CLEANING_AGE = 1
CLEANING_INTERVAL = 0.1

# Set up CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/profile/{profile_id}")
async def read_results(profile_id: str):
    profile_result = profile_store.get_profile(profile_id)
    profile_result['timestamp'] = profile_result['timestamp'].isoformat()
    return Response(content=json.dumps(profile_result))

@app.post("/api/profile")
async def profile_file(files: List[UploadFile]):
    profile_id = await profile_store.create_profile(files[0])
    response = {'profile_id': profile_id}
    return Response(content=json.dumps(response))

@app.on_event('startup')
async def schedule_profile_cleaner():
    async def run():
        while True:
            cleaning_ts = datetime.datetime.now() - datetime.timedelta(minutes=CLEANING_AGE)
            deleted_profile_ids = profile_store.clean_profiles(cleaning_ts)
            logger.info('cleaned profiles:', deleted_profile_ids)
            await asyncio.sleep(CLEANING_INTERVAL * 60)

    asyncio.create_task(run())