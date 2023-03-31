# Profiler

## Setup
Python version 3.10+

```
# create virtual env
python -m venv env
source env/bin/activate

# Install packages
pip install -r requirements.txt
```

## API

Launch the web app:
```
uvicorn api:app --reload
```


### Profile
1. Head over to where the server is running.
2. Upload a CSV file
3. Check out the results

### Share
1. Copy the browser URL and share it :)

## CLI

```
python cli.py -i <CSV input file>
```

Result is created to `profile_results` as an HTML file.