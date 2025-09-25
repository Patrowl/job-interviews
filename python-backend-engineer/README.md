# Link shortener
A simple Django + DRF-based link shortener that generates short codes for redirects and provides an API to create and retrieve short links.

## Local deployment

### Install mise
Follow the instructions at [https://mise.jdx.dev/getting-started.html](https://mise.jdx.dev/getting-started.html) 

### Set up and activate the environment
```bash
cd python-backend-engineer
mise trust
```
Specific version of Python and Poetry will be installed in the current folder, and a Python virtual environment will be created and activated.

### Install dependencies
```bash
poetry install
```

### Apply migrations
```bash
python manage.py migrate
```

### Run the app
```bash
python manage.py runserver
```
The app will be available on http://localhost:8000.

## Documentation
Interactive documentation is available on:
* http://localhost:8000/api/docs (Swagger UI)
* http://localhost:8000/api/redoc (Redoc)
