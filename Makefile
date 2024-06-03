IMAGE_NAME?=letsrolld
DB=$(PWD)/movie.db
DIRECTORS_NUMBER?=10
DIRECTORS_FILE?=directors.csv
RUN_LOG?=run.log
RUN_LOG_CMD?=ts | tee -a $(RUN_LOG)

.PHONY: install lint mypy test populate run-update-directors run-update-films run-update-offers run-cleanup run-all run-db-upgrade webapp ui swagger swagger_py get-dirs get-films

install:
	pdm install -v

lint: install swagger
	pre-commit run --all-files

mypy:
	pdm run mypy . --exclude alembic/env.py --exclude src/letsrolld/db/models.py

test: lint
	pdm run pytest

populate:
	pdm run populate-directors -d ${DIRECTORS_FILE} -n ${DIRECTORS_NUMBER}

run-update-directors:
	pdm run update-directors $(ARGS) | $(RUN_LOG_CMD)

run-update-films:
	pdm run update-films $(ARGS) | $(RUN_LOG_CMD)

run-update-offers:
	pdm run update-offers $(ARGS) | $(RUN_LOG_CMD)

run-cleanup:
	pdm run cleanup $(ARGS) | $(RUN_LOG_CMD)

run-all: run-update-directors run-update-films run-update-offers run-cleanup

run-db-upgrade:
	pdm run alembic upgrade head

webapp:
	pdm run webapp

swagger:
	#curl http://localhost:8000/api/doc/swagger.json -o swagger.json
	pdm run swagger > swagger.json
	openapi-generator-cli validate -i swagger.json

swagger_py: swagger
	pdm run openapi-python-client generate --path swagger.json

ui:
	cd ui && http-server --port 8081 -c-1 -o

get-dirs:
	pdm run lcli directors get

get-films:
	pdm run lcli films get
