bash:
	docker exec -it djangoplicity-events bash

test:
	docker exec -it djangoplicity-events coverage run --source='.' manage.py test

coverage-html:
	docker exec -it djangoplicity-events coverage html
	open ./htmlcov/index.html

futurize-stage1:
	docker exec -it djangoplicity-events futurize --stage1 -w -n .

futurize-stage2:
	docker exec -it djangoplicity-events futurize --stage2 --nofix=newstyle -w -n .

test-python27:
	tox -e py27-django111
