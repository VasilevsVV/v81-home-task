pip-install:
	.venv/bin/python -m pip install labelbox matplotlib numpy pandas pathlib

clean:
	rm -rf ./output/

.PHONY: pip-install