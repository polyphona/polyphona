# Polyphona

A familiar, portable music editor for your desktop.

## Install

### Client

Make sure you have [Node] ad [npm] installed, then run:

```bash
npm install
```

### Server

Install dependencies using pip (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

## Usage

### Presentation of the backend server

The server stores songs and user data. The desktop app uses its REST API
to display and manipulate data.

It consists in:

- A web application server, written in Python using Falcon (a REST API framework) and running on Gunicorn (or a similar process manager);
- A database module, also written in Python and backed by SQLite and the `sqlite3` module.

The database itself is stored in a file named `polyphona_db.db`. If no file is found a new one will be created upon the launch of the server.

### Running the server

To run the server locally, run the following command from the project root directory:

```bash
gunicorn api:app
```

For more advanced use cases, please refer to the Gunicorn documentation or the process manager you are using.

### Running the desktop app

To run the desktop app, run:

```bash
npm run dev
```

in the root directory.

## Tests

The server comes with a test suite written with Pytest.

To run the test suite, run `$ pytest` from the project root directory.

## Resources

To get started with Electron, read [Writing your first Electron app](https://electronjs.org/docs/tutorial/first-app).

[node]: https://nodejs.org/en/
[npm]: https://www.npmjs.com/get-npm
[falcon]: https://falcon.readthedocs.io/en/stable/
[gunicorn]: https://gunicorn.org/
[sqlite3]: https://docs.python.org/3.4/library/sqlite3.html
[pytest]: https://docs.pytest.org/en/latest/
[pip]: https://pypi.org/project/pip/
