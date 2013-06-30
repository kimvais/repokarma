sync:
	@python sync.py

sync-all: clean-db sync

clean-db:
	@rm data.sqlite3
	@python manage.py syncdb
	@python manage.py migrate repokarma
