from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from profiler import ProfileStore
from typing import List
import logging

app = FastAPI()
logger = logging.getLogger(__name__)
profile_store = ProfileStore()

@app.get("/", response_class = HTMLResponse)
def index():
    f = open(f'frontend/index.html', "r")
    return f.read()

@app.get("/profile/{profile_id}", response_class = HTMLResponse)
def read_results(profile_id: str):
    profile_file = profile_store.get_profile(profile_id)
    return profile_file.read()

@app.post("/profile/")
def profile_file(files: List[UploadFile]):
    profile_id = profile_store.create_profile(files[0])
    return {'profile_id': profile_id}
