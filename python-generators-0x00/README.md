# Python Generators — user data streaming and pagination

This repository demonstrates simple examples of using Python generators to stream and paginate user data stored in a PostgreSQL database. The code is educational and shows several patterns:

- streaming rows one-by-one from a DB cursor
- streaming rows in batches
- lazy pagination using LIMIT/OFFSET
- computing streaming aggregates (average age)
- seed utilities to create DB, table and insert CSV data

Files
-----

- `seed.py` — helper utilities for connecting to PostgreSQL, creating the database/table and inserting data from `user_data.csv`.
- `user_data.csv` — sample CSV dataset used by `seed.py` to populate the `alx_users` table.
- `0-main.py` — example script that runs the seed flow: create DB/table and insert data; prints a couple of rows to confirm.
- `0-stream_users.py` — generator `stream_users()` that yields rows from `alx_users` one at a time.
- `1-batch_processing.py` — provides `stream_users_in_batches(batch_size)` which yields batches of rows (`fetchmany`) and `batch_processing(batch_size)` which demonstrates filtering (users with age > 40).
- `1-main.py` — small runner that prints the first 6 users using `itertools.islice` on `stream_users()`.
- `2-lazy_paginate.py` — contains `paginate_users(page_size, offset)` and `lazy_pagination(page_size)` which yields pages (lists of rows) using LIMIT/OFFSET.
- `2-main.py` — example runner that iterates pages from `lazy_pagination` and prints rows.
- `3-main.py` — runner that calls `batch_processing(50)` (demonstrates batch processing usage and handles BrokenPipeError when piping output).
- `4-stream_ages.py` — provides `stream_user_ages()` (yields each user's age) and `stream_average_user_ages()` (computes and yields the overall average age — note: implementation yields the final average once the iteration completes).

Quick overview / contract
-------------------------

Inputs
- PostgreSQL server reachable using credentials in `seed.py`.
- `user_data.csv` present in the project root when seeding data.

Outputs
- SQL tables and rows inserted into the `ALX_prodev` database (table: `alx_users`).
- Console output from the example runner scripts.

Success criteria
- Able to connect to Postgres, create DB/table and insert data.
- The generator scripts yield rows/pages as described and example mains print sample rows.

Prerequisites
-------------

- Python 3.8+
- PostgreSQL server running locally (or reachable remotely).
- psycopg2 (or psycopg2-binary) installed.

Installing dependencies (Debian/Ubuntu example)

```bash
# system deps required for psycopg2 (if building from source)
sudo apt update
sudo apt install -y python3-dev libpq-dev build-essential

# create a venv and install Python deps
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install psycopg2-binary
```

Configuration
-------------

Edit `seed.py` and update the `CONFIG` and `DB_CONFIG` dictionaries to match your PostgreSQL host, port, user, password and database name. By default the repository uses local defaults:

- `CONFIG` is used to connect to the server for database creation.
- `DB_CONFIG` is used to connect to the `ALX_prodev` (or configured) database for creating tables and inserting data.

Usage
-----

1) Seed the database and insert CSV data

```bash
# from project root
python3 0-main.py
```

This script calls the `seed` helpers to create the database/table (if they don't exist) and insert rows from `user_data.csv`.

2) Stream single rows

```bash
python3 1-main.py
```

3) Batch processing example (filtering users older than 40)

```bash
python3 3-main.py
```

4) Lazy pagination example (iterate pages of users)

```bash
python3 2-main.py
```

5) Streaming ages and computing average

Use the functions provided in `4-stream_ages.py` from a script or REPL. Note: current implementation yields the final average once it has iterated all ages.

Notes, edge cases and caveats
----------------------------

- The code assumes a PostgreSQL server and uses `psycopg2`.
- The `create_database` implementation in `seed.py` uses a SQL string `CREATE DATABASE IF NOT EXISTS ALX_prodev;` — Postgres does not support `IF NOT EXISTS` for CREATE DATABASE prior to some versions; you may need to adjust or create the DB manually. Alternatively connect as a superuser and create the database before running the seeding.
- `stream_average_user_ages()` currently computes average with the accumulator and yields only once after iterating all ages. If you want a running average emitted after every row, move the `yield average_age` inside the loop.
- Be careful with large CSVs and memory: `insert_data` uses streaming from CSV (DictReader) and individual INSERTs — for large datasets consider COPY or batched INSERTs.

Troubleshooting
---------------

- If psycopg2 fails to install: try `pip install psycopg2-binary` instead of `psycopg2`.
- If connection fails, verify `host`, `port`, `user`, `password` and that PostgreSQL is running and allowing connections from your host.

Suggested next steps
--------------------

1. Add unit tests (pytest) for generator functions using a small in-memory SQLite or a test Postgres instance.
2. Improve `seed.create_database` to use Postgres-compatible existence checks or create the DB outside the script.
3. Add a CLI (argparse / click) to the runner scripts so page sizes / batch sizes and DB config can be passed via CLI.
4. Use connection pooling (psycopg2 pool) for more realistic performance tests.

License
-------
This repository is provided for educational purposes.

---

If you want, I can also:
- add a small CLI wrapper for the examples,
- fix the `stream_average_user_ages()` to yield a running average, or
- add tests and a `requirements.txt`.
Tell me which you'd like next.

