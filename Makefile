.PHONY: test

test:
	@python3 -m unittest -v

requirements:
	@pip install -r requirements.txt
