# Polyphona

A familiar, portable music editor for your desktop. 

## Install

### Client

Make sure you have [Node] ad [npm] installed, then run:

``` bash
npm install
```

### Server

Install dependencies using pip (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

## Presentation

## Usage

### Presentation of the backend server

The server stores songs and user data. The desktop app uses its REST API
to display and manipulate data.

It consists in:

- A web application server, written in Python using Falcon and running on Gunicorn (or a similar process manager);
- A database module, also written in Python and backed by SQLite3.

The database itself is stored in a file named `server/polyphona_db.db`.
If no file is found a new one will be created upon the launch of the server.

### Running the server

To run the server locally, `cd` to the `server` directory and use:

```bash
gunicorn server:app
```

For more advanced use cases, please refer to the gunicorn documentation or whatever service you want to use instead.

### Running the desktop app

To run the desktop app, run:

```bash
npm run dev
```

in the root directory.

## Tests

The server includes a `server_test.py` file, that allows for thorough testing through pytest.

To run the test, you need to first delete the database file (or rename it if it is contains valuable data), then run:

``` bash
pytest
```

## Resources

To get started with Electron, read [Writing your first Electron app](https://electronjs.org/docs/tutorial/first-app).

[Node]: https://nodejs.org/en/
[npm]: https://www.npmjs.com/get-npm
[Falcon]: https://falcon.readthedocs.io/en/stable/
[gunicorn]: https://gunicorn.org/
[sqlite3]: https://docs.python.org/3.4/library/sqlite3.html
[pytest]: https://docs.pytest.org/en/latest/
[pip]: https://pypi.org/project/pip/
