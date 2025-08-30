#!/bin/bash 

set -o errexit

set -o nounset

set -o pipefail


python << END 
import sys 
import time 
import psycopg2

suggest_unavailable = 30 

start_time = time.time()
while True: 
    try: 
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}"
        )
        break
    except psycopg2.OperationalError as e:
        sys.stderr.write(f"Waiting for PostgreSQL...: {e}\n")
        if time.time() - start_time > suggest_unavailable:
            sys.stderr.write(f"PostgreSQL is unavailable. The following error occurred: {e}\n")
            sys.exit(1)
        time.sleep(3)

END

echo >&2 "PostgreSQL is available. Starting Django server..."

exec "$@"

