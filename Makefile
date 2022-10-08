env-dev:
	test -d venv || python3 -m venv venv
	. venv/bin/activate; \
	pip install -U pip setuptools wheel; \
	pip install -r app/requirements.in

env-clean:
	rm -rf venv

copy:
	cp -r app/ docker_debian/app