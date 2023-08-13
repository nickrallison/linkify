default: 
	@python src/main.py notes

clean_files:
	@python src/main.py clean

tests:
	@python src/main.py test