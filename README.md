# Climate Change & Bikeability News Search (Exercise 5)

Simple search application with Elasticsearch (Docker) and Flask.

## Files
- `documents.json` - the 20 news texts
- `docker-compose.yml` - starts Elasticsearch 8.15.3
- `create_index.py` - creates the index `news` and loads the documents
- `app.py` - web server and the three query logics (Boolean AND, Ranked OR, Phrase)
- `templates/index.html` - user interface

## Start
```bash
docker compose up -d                 # start Elasticsearch
python3 -m venv .venv                # first time only
source .venv/bin/activate            # every new terminal
pip install -r requirements.txt      # first time only
python create_index.py               # load documents
python app.py                        # open http://localhost:5000
```
