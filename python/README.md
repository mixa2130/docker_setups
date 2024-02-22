# Poetry

## Install
Poetry simplifies managing dependencies by supporting groups within one file. This allows you to keep track of all dependencies in a single place.

~~~bash
$ poetry add numpy pandas
$ poetry add --group dev pytest pre-commit
~~~

~~~toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.8"
pandas = "^2.0"
numpy = "^1.24.3"

[tool.poetry.group.dev.dependencies]
pytest = "^7.3.2"
pre-commit = "^3.3.2"
~~~

To install only production dependencies:

~~~bash
$ poetry install --only main
~~~

To install both development and production dependencies:
~~~bash
$ poetry install
~~~

## Uninstall

Poetry also removes the package and its dependencies.

~~~bash
$ poetry add pandas

$ poetry remove pandas

  • Removing numpy (1.24.3)
  • Removing pandas (2.0.2)
  • Removing python-dateutil (2.8.2)
  • Removing pytz (2023.3)
  • Removing six (1.16.0)
  • Removing tzdata (2023.3)
~~~

Update lock dependencies
~~~bash
poetry lock
~~~