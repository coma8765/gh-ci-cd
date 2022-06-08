help:
	echo test
	echo build

test:
	pipenv run pytest app -vv

build:
	set -e

	docker build \
	  -t docker.aa12.ml/redled/api:${V} \
	  -t docker.aa12.ml/redled/api:latest \
	  .

	docker image push docker.aa12.ml/redled/api -a

	docker build \
	  -t docker.aa12.ml/redled/api-test:${V} \
	  -t docker.aa12.ml/redled/api-test:latest \
	  --target test \
	  .

	docker image push docker.aa12.ml/redled/api-test -a
