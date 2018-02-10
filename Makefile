all: init multiple test visualization
init:
		python __init__.py
multiple:
		python multiple_snapshot.py
test:
		python multiple_timing.py
visualization:
		python visualize.py