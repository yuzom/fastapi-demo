## How to run this program

### Setup a virtual environment

In terminal directory:
python3 -m venv venv

In command palette:
> python select interpreter
> enter interpreter path
> ./venv/bin/python

### Activate the virtual environment

In terminal directory:
source venv/bin/activate

### Install requirements

pip install -r requirements.txt

### Start the webserver

uvicorn app.main:app
or
uvicorn app.main:app --reload

## Notes

### Fast API

Fast API decorator specifies the path, response schema, and success status codes for the function it decorates
The function itself is passed the input schema and dependencies like:
* Database sessions
* User authentication

Dependency functions allow FastAPI to execute common tasks and return their values before calling the main function
* This allows for separation of concerns and automatic documentation
* And sharing common objects like the database

Path operation = route

Http request methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
* GET = retrieve data
* HEAD = GET but without a response body
* POST = submit data
* PUT = replace target with requested payload
* DELETE = deletes target
* CONNECT = establish a tunnel to the server

FastAPI runs whichever URL it encounters first in the file (order matters)

Use Postman to test your API without building a frontend

FastAPI allows you to explicitly define the schema (format) your user can send the data to, otherwise return an error, by using pydantic

### CRUD, HTTP request, URL, and decorator best practices

Create
* POST      /posts          @app.post("/posts")

Read
* GET       /posts/:id      @app.get("/posts{id}")
* GET       /posts          @app.get("/posts")

Update
* PUT/PATCH /posts/:id      @app.put("/posts{id}")

Delete
* DELETE    /posts/:id      @app.delete("/posts{id}")

### DBMS

Never talk to a database directly, use a DBMS
Relational (MYSQL, POSTGRESQL, etc) or NoSQL (MongoDB, DynamoDB, etc)

In PostgreSQL, use Not NULL rule to prevent blank entries in DB

### ORM

Allows you to CRUD rows and tables in python instead of SQL
Most popular is SQLalchemy

### SQLalchemy

models.py contains the table schema
database.py contains the helper code to start a DB session
When creating a table using SQLalchemy, it will look for tables of the same name
And if none are found, it creates the table
It cannot update table schema, so manually delete the table to make schema changes

### Schemas

Pydantic model defines how a request and response should look like (transfer)
* Pydantic performs variable validation and conversion

SQLalchemy model defines the columns and rules of the DB schema (DB)

### Authentication

JWT token based authentication is stateless (does not store info whether user is logged in or not)
Client side stores information

1. Client provides username and password to API
2. If credentials are valid, API sends a token
3. Client tries a CRUD operation with the token appended to the header
4. If token is valid, API performs action and returns data

Components of JWT token:
* Header (signing algorithm, token type)
* Payload (user ID, role, etc)
* Signature (API-side secret)

Important: JWT tokens are not encrypted

How a token is made:
* Header, payload, and secret are hashed to create a signature
* The header, payload, and signature make up a token and is sent to the API

How a token is verified:
* Header, payload, and secret are hashed to create a test signature on API-side
* The client signature is compared with the test signature

We use the python-jose library based off pyjwt for token authentication

Check the return token here: https://jwt.io/
FastAPI docs on using JWT: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ (we use a different library)

### Login

* Client sends email, plain text password
* API finds the user and their hashed password on the DB
* Clients password is hashed then compared to DB hashed password

We use the passlib.context library's CryptContext module to compare a user input plain text password against the DB stored hashed password

### Postman shortcuts

Create an environment and add a URL variable to make it easy to switch between dev and prod URLs
Call the variable using {{URL}}
Add a token variable using a post-res script for Login get request: pm.environment.set("JWT", pm.response.json().access_token);

### Postman query parameters

Pass query parameters into Fast API by directly adding it into the function call
In postman, append ?<parameter>=<value> to the query
* Add additional query parameters with &
* Add space to a search using %20

Example for GET POSTS: {{URL}}posts?limit=2&skip=0&search=2

### Environment variables

Add all environmental variables into .env
config.py contains a pydantic settings class which loads, validates, and converts all env variables found in .env
Why not just use os and load_dotenv functions?
* So that we can validate that all env variables are correctly passed before running the program
* This method works in production environments

### Composite keys

Use a PK that corresponds multiple columns to make sure each post cannot be voted by more than one user

### Joins

Note that while SQL join is a left outer join by default, SQLalchemy join is a left inner joint

### Database migrations using alembic

Install alembic:
pip install alembic

Initialize alembic to create directory:
alembic init alembic

Modify env.py with:
from app.models import Base
from app.config import settings
config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}")
target_metadata = Base.metadata

Create posts table:
alembic revision -m "create posts table"
And update def upgrade() and def downgrade()

To go to an alembic db history:
alembic upgrade <revision_no>

To upgrade:
alembic upgrade head

To downgrade:
alembic downgrade -1

Auto-generate feature:
Alembic can figure out what columns and tables are missing between the sqlalchemy model and postgres db, and make the changes without needing to drop the current tables
alembic revision --autogenerate -m "<insert_comment_here>"
alembic upgrade head

### CORS (Cross Origin Resource Sharing)

Allows you to make requests from a web browser on one domain to a server on a different domain
By default, FastAPI only allows browsers running on the same domain as our server to make requests to it

### Git initialization instructions

Create a repo on github

In terminal:
git init
git add --all
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/<your_username>/<your_repo_name>.git
git push -u origin main

### Heroku

Install Heroku and create a free account; use a github student discount for 24mo free access

In terminal:
heroku login
heroku create fastapi-<your_name>
git push heroku main

### Git update instructions

git add --all
git push origin main
git push heroku main

### Troubleshoot heroku

heroku logs -t

### Create heroku postgres db

heroku addons:create heroku-postgresql:essential-0
Set environment variables by going to https://dashboard.heroku.com/apps/<your_app_name>/settings
Get the variable names from your postgres instance settings

Restart heroku instance (dyno):
heroku ps:restart

Get your API URL:
heroku apps:info <app_name>