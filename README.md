# About CrateDB

[![Bluesky][badge-bluesky]][project-bluesky]

[![CI][badge-ci]][project-ci]
[![Coverage][badge-coverage]][project-coverage]
[![License][badge-license]][project-license]
[![Release Notes][badge-release-notes]][project-release-notes]

[![Status][badge-status]][project-pypi]
[![PyPI Version][badge-package-version]][project-pypi]
[![Python Versions][badge-python-versions]][project-pypi]
[![Downloads per month][badge-downloads-per-month]][project-downloads]

» [Documentation]
| [Releases]
| [Issues]
| [Source code]
| [License]
| [CrateDB]
| [Community Forum]

A high-level description about [CrateDB], with cross-references
to relevant resources in the spirit of a curated knowledge backbone.

> CrateDB is a distributed and scalable SQL database for storing and
> analyzing massive amounts of data in near real-time, even with
> complex queries. It is based on Lucene, inherits technologies from
> Elasticsearch, and is compatible with PostgreSQL.

## What's inside

- A few tidbits of _structured docs_.

- The [cratedb-outline.yaml] file indexes documents about what CrateDB is
  and what you can do with it.

- The [about/v1] folder includes [llms.txt] files generated from
  [cratedb-outline.yaml] by expanding all links. They can be used
  to provide better context for conversations about CrateDB.

## Install

### From PyPI
```shell
uv tool install --upgrade 'cratedb-about[all]'
```
### From Repository
```shell
uv tool install --upgrade 'cratedb-about[all] @ git+https://github.com/crate/about'
```

## Usage

### Outline

#### CLI
Convert knowledge outline from `cratedb-outline.yaml` into Markdown format.
```shell
cratedb-about outline --format=markdown > outline.md
```

#### API
Use the Python API to retrieve individual sets of outline items, for example,
by section name. The standard section names are: Docs, API, Examples, Optional.
The API can be used to feed information to a [Model Context Protocol (MCP)]
documentation server, for example, a subsystem of [cratedb-mcp].
```python
from cratedb_about import CrateDbKnowledgeOutline

# Load information from YAML file.
outline = CrateDbKnowledgeOutline.load()

# List available section names.
outline.get_section_names()

# Retrieve information about resources from the "Docs" and "Examples" sections.
outline.find_items(section_name="Docs", as_dict=True)
outline.find_items(section_name="Examples", as_dict=True)

# Convert outline into Markdown format.
outline.to_markdown()
```

### llms-txt

#### Build
The Markdown file `outline.md` serves as the source for generating the `llms.txt` file.
```shell
llms_txt2ctx --optional=true outline.md > llms-full.txt
```

Generate multiple `llms.txt` files along with any auxiliary output files.
```shell
export OUTDIR=./public_html
cratedb-about build
```

#### Query
Ask questions about CrateDB from the command line.
#### CLI
```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
cratedb-about ask "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```
#### API
Use the Python API to ask questions about CrateDB.
```python
from cratedb_about import CrateDbKnowledgeConversation

knowledge = CrateDbKnowledgeConversation()
knowledge.ask("CrateDB does not seem to provide an AUTOINCREMENT feature?")
```

If you are running out of questions, get inspired by the standard library.
```shell
cratedb-about list-questions
```

To configure a different context file, use the `CRATEDB_CONTEXT_URL` environment
variable. The default value is https://cdn.crate.io/about/v1/llms-full.txt.

## Project Information

### Acknowledgements
Kudos to the authors of all the many software components and technologies
this project is building upon.

### Contributing
The `cratedb-about` package is an open source project, and is [managed on
GitHub]. Contributions of any kind are very much appreciated.


[about/v1]: https://cdn.crate.io/about/v1/
[CrateDB]: https://cratedb.com/database
[cratedb-mcp]: https://github.com/crate/cratedb-mcp
[cratedb-outline.yaml]: https://github.com/crate/about/blob/main/src/cratedb_about/outline/cratedb-outline.yaml
[llms.txt]: https://llmstxt.org/
[Model Context Protocol (MCP)]: https://modelcontextprotocol.io/introduction

[Community Forum]: https://community.cratedb.com/
[Documentation]: https://github.com/crate/about
[Issues]: https://github.com/crate/about/issues
[License]: https://github.com/crate/about/blob/main/LICENSE
[managed on GitHub]: https://github.com/crate/about
[Source code]: https://github.com/crate/about
[Releases]: https://github.com/crate/about/releases

[badge-bluesky]: https://img.shields.io/badge/Bluesky-0285FF?logo=bluesky&logoColor=fff&label=Follow%20%40CrateDB
[badge-ci]: https://github.com/crate/about/actions/workflows/main.yml/badge.svg
[badge-coverage]: https://codecov.io/gh/crate/about/branch/main/graph/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/cratedb-about/month
[badge-license]: https://img.shields.io/github/license/crate/about.svg
[badge-package-version]: https://img.shields.io/pypi/v/cratedb-about.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/cratedb-about.svg
[badge-release-notes]: https://img.shields.io/github/release/crate/about?label=Release+Notes
[badge-status]: https://img.shields.io/pypi/status/cratedb-about.svg
[project-bluesky]: https://bsky.app/search?q=cratedb
[project-ci]: https://github.com/crate/about/actions/workflows/tests.yml
[project-coverage]: https://app.codecov.io/gh/crate/about
[project-downloads]: https://pepy.tech/project/cratedb-about/
[project-github]: https://github.com/crate/about
[project-license]: https://github.com/crate/about/blob/main/LICENSE
[project-pypi]: https://pypi.org/project/cratedb-about
[project-release-notes]: https://github.com/crate/about/releases
