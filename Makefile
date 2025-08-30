up-build:
	docker compose -f local.yml up --build -d --remove-orphans

up: 
	docker compose -f local.yml up -d --remove-orphans

down: 
	docker compose -f local.yml down

down-v: 
	docker compose -f local.yml down -v

config: 
	docker compose -f local.yml config

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --noinput --clear

shell:
	docker compose -f local.yml run --rm api python manage.py shell

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

flush: 
	docker compose -f local.yml run --rm api python manage.py flush

network-inspect: 
	docker network inspect finance_backend_local_nw

finance_db: 
	docker compose -f local.yml exec postgres psql --username=postgres --dbname=finance_db

apilogs:
	docker compose -f local.yml logs -f api

pglogs:
	docker compose -f local.yml logs -f postgres

mailpitlogs:
	docker compose -f local.yml logs -f mailpit

logs:
	docker compose -f local.yml logs 


# run as local user