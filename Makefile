install:
	./.github/add_github_hooks.sh
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black $$(git ls-files "*.py")

lint:
	pylint --disable=R,C $$(git ls-files "*.py")

test:
#	pytest -vv --cov-report term-missing --cov=. testing/
	echo "No tests required"
all: install format lint test