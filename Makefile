init:
	pip install -r requirements.txt

test:
	python -m unittest discover

lint:
	pylint trains/{core,__main__}.py

clean:
	find . -name '*.pyc' -delete
