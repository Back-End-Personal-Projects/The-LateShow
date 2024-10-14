# The LateShow API
Welcome to the Late Show API! This API allows you to manage episodes, guests, and their appearances on a late-night show. It provides endpoints for creating, reading, updating, and deleting episodes, guests, and appearances.
# Features
-  Episodes: Retrieve, create, update, and delete episodes.
-  Guests: Manage guests with their details and appearances.
-  Appearances: Track guest appearances on episodes along with ratings.
# Technologies Used
-  Flask: A lightweight WSGI web application framework for Python.
-  Flask-SQLAlchemy: An extension that adds SQLAlchemy support to Flask applications.
-  Flask-Migrate: Handles SQLAlchemy database migrations for Flask applications.
-  SQLite: A lightweight database for development and testing.
-  Postman: For testing the API endpoints.
# Set Up
Run these commands to install the dependencies and set up the database:

- pipenv install
- pipenv shell
- cd server
- export FLASK_APP=app.py
- export FLASK_RUN_PORT=5555
- pip install Flask-Migrate
- pip install sqlalchemy-serializer
- pip install faker
- flask db init
- flask db migrate -m 'initial migration'
- flask db upgrade head
- python app.py
- python seed.py
- flask run

You can view the models in the server/models.py module, and the migrations in the server/migrations/versions directory.
# API Endpoints
## Episodes
-  GET /episodes: Retrieve all episodes.
- GET /episodes/<int:id>: Retrieve a specific episode by ID.
- POST /episodes: Create a new episode.
- PUT /episodes/<int:id>: Update a specific episode.
- PATCH /episodes/<int:id>: Partially update a specific episode.
- DELETE /episodes/<int:id>: Delete a specific episode.
## Guests
- GET /guests: Retrieve all guests.
- GET /guests/<int:id>: Retrieve a specific guest by ID.
- POST /guests: Create a new guest.
- PUT /guests/<int:id>: Update a specific guest.
- PATCH /guests/<int:id>: Partially update a specific guest.
- DELETE /guests/<int:id>: Delete a specific guest.
## Appearances
- GET /appearances: Retrieve all appearances.
- GET /appearances/<int:id>: Retrieve a specific appearance by ID.
- POST /appearances: Create a new appearance.
- PUT /appearances/<int:id>: Update a specific appearance.
- PATCH /appearances/<int:id>: Partially update a specific appearance.
- DELETE /appearances/<int:id>: Delete a specific appearance.
# Testing with Postman
You can use Postman to test the API endpoints. Import the provided Postman collection to get started with pre-defined requests.