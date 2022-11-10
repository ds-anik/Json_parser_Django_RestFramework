# Json Parser

Write a Python code that takes a JSON string as an input, transforms it into another JSON format, and saves the result as a JSON field in a Postgres DB.
Please read "Python Assignment.pdf" for more instructions.

## Set up

If you are on linux install postgres and run  `./init.sh` to initialize otherwise install packages listed in
requirements.txt set up your database as

- user `location_assignment_user`
- password `some_password`
- db_name `location_assignment`
- Also grant all privileges on that database to that user

```sql
GRANT ALL PRIVILEGES ON DATABASE location_assignment TO location_assignment_user;
alter user location_assignment_user createdb; --- this one is required in order to run tests 
```

then migrate the database

```shell
python manage.py migrate
```

## Running

You can run the application with

```shell
python manage.py runserver
```

then you can point your browser to `http://127.0.0.1:8000/create/` and use the UI or use `curl` to test the application

```shell
curl --location --request POST 'http://127.0.0.1:8000/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "address": "https://www.google.com ",
    "content": {
        "seasons": [
            {
                "text": "winter"
            },
            {
                "text": "spring"
            },
            {
                "text": "summer"
            },
            {
                "text": "autumn"
            }
        ],
        "description": "All seasons"
    },
    "updated": "2021-02-26T08:21:20+00:00",
    "author": {
        "username": "Bob",
        "id": "68712648721648271"
    },
    "id": "543435435",
    "created": "2021-02-25T16:25:21+00:00",
    "counters": {
        "A": 3,
        "B": 0
    },
    "type": "main"
}'
```

## Running tests

Simply run ```python manage.py test --noinput```

## Database Inspection

At last, you can also check out the admin area but first you'd need to create an admin user

```shell
python manage.py createsuperuser
```

fill out the required data then head to `http://127.0.0.1:8000/admin`
