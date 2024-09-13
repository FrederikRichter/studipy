rm dist/*
poetry build
poetry run pip install dist/$(ls dist/ | grep .whl)
poetry run python tests.py
