

# Polyphona

A familiar, portable music editor for your desktop. 

#### Build Setup

Make sure you have [Node] ad [npm] installed.

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:9080
npm run dev

# build electron application for production
npm run build


# lint all JS/Vue component files in `src/`
npm run lint

```


#### Back Setup
## Requirements
All requirements are in the requirements.txt file, usable through pip:
``` bash
pip install -r requirements
```

## Presentation
The server is composed of a web server, written in python, using Falcon and running on gunicorn (or similar service); and a database, also written in python and using sqlite3.
The database itself is stored in a file named `server/polyphona_db.db`, if no file is found a new one will be created upon the launch of the server.

## Running the server
To run the server locally, use:
``` bash
gunicorn server:app
```

For more advanced use cases, please refer to the gunicorn documentation or whatever service you want to use instead.

## Test
The server includes a `server_test.py` file, that allows for thorough testing through pytest.
To run the test, you need to first delete the database file (or rename it if it is contains valuable data), then simply run:
``` bash
pytest
```




To get started with Electron, read [Writing your first Electron app](https://electronjs.org/docs/tutorial/first-app).

[Node]: https://nodejs.org/en/
[npm]: https://www.npmjs.com/get-npm
[Falcon]: https://falcon.readthedocs.io/en/stable/
[gunicorn]: https://gunicorn.org/
[sqlite3]: https://docs.python.org/3.4/library/sqlite3.html
[pytest]: https://docs.pytest.org/en/latest/
[pip]: https://pypi.org/project/pip/
