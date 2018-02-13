all: clean run 

run: queries single multiple test visualization 

test: timing random

queries:
	python make_queries.py
single:
	python single_snap.py
multiple:
	python multiple_snapshot.py
timing:
	python multiple_timing.py
random:
	python random_multiple.py
visualization:
	python visualize.py
clean:
	python __init__.py
