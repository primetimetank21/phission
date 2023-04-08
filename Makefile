install:
	./.github/add_github_hooks.sh
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black $$(git ls-files "*.py")

lint:
	pylint --disable=R,C $$(git ls-files "*.py")

all: install format lint