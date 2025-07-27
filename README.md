# About CrateDB

[![Status][badge-status]][project-pypi]
[![CI][badge-ci]][project-ci]
[![Coverage][badge-coverage]][project-coverage]
[![Downloads per month][badge-downloads-per-month]][project-downloads]

[![License][badge-license]][project-license]
[![Release Notes][badge-release-notes]][project-release-notes]
[![PyPI Version][badge-package-version]][project-pypi]
[![Python Versions][badge-python-versions]][project-pypi]

» [Documentation]
| [Releases]
| [Issues]
| [Source code]
| [License]
| [CrateDB]
| [Community Forum]
| [Bluesky]

A high-level description about [CrateDB], with cross-references
to relevant resources in the spirit of a curated knowledge backbone.

> CrateDB is a distributed and scalable SQL database for storing and
> analyzing massive amounts of data in near real-time, even with
> complex queries. It is based on Lucene, inherits technologies from
> Elasticsearch, and is compatible with PostgreSQL.

## What's inside

A workbench rig for information and knowledge management,
aiming to compress content authoring and curation processes,
nothing big.

### Abstract

- **Structured documentation** based on a basic and generic [hierarchical outline].

- **Utility programs** to parse [YAML] outline files and generate outputs
  (e.g., [Markdown], [llms-txt]), supporting the authoring and
  production process.

- **Python API** that offers selective access to documentation
  and knowledge resources by providing basic querying primitives to
  inquire elements from the outline tree.

### Applied

- The `ask` subcommand uses [llms-txt] context files to answer questions
  about a topic domain that would otherwise yield incomprehensible,
  incomplete, or weak responses.

- The compact Python API can be used by a [Model Context Protocol (MCP)]
  documentation server to acquire information about the relevant topic
  domain on demand.

### Concrete

- The outline file [cratedb-outline.yaml] file indexes documents about
  what CrateDB is, what you can do with it, and how.

- The Markdown file [instructions.md] includes instructions and
  directives about how to use CrateDB. They can be used by humans as a
  cheat sheet, or to improve prompts for LLMs and similar technologies.

- Context bundle files are published to the [about/v1] folder.
  They can be used to provide better context for conversations about
  CrateDB, for example, by using the `cratedb-about ask` subcommand,
  or by using generic applications like [`llm`].

- The documentation subsystem of the [cratedb-mcp] package uses the
  Python API to serve and consider relevant documentation resources
  within its data flow procedures. It selects relevant resources mostly
  based on the value of the `description` attribute of the outline
  data model.

## Install

The authors recommend using the [uv] package manager. Alternative
options are to use `pipx` or `pip install --user`.

### From PyPI
```shell
uv tool install --upgrade 'cratedb-about[all]'
```
### From Repository
```shell
uv tool install --upgrade 'cratedb-about[all] @ git+https://github.com/crate/about'
```

## Usage

The `cratedb-about` package provides three subsystems.

- Outline: Read and inquire outline files.
- Bundle: Produce a context bundle from an outline file.
- Query: Use context information for conversations with LLMs.

### Outline

#### CLI
Convert knowledge outline from built-in `cratedb-outline.yaml` into Markdown format.
```shell
cratedb-about outline --format="markdown" > outline.md
```
Use the `llms-txt` format to directly generate [llms-txt] compatible output.
```shell
cratedb-about outline --format="llms-txt" > llms.txt
```
Use the `--optional` flag to include the "Optional" section for
generating the `llms-full.txt` file.
```shell
cratedb-about outline --format="llms-txt" --optional > llms-full.txt
```

Use a custom outline file on a local or remote filesystem.
```shell
cratedb-about outline --url https://github.com/crate/about/raw/refs/heads/main/src/cratedb_about/outline/cratedb-outline.yaml
```
When using this option, you will need to minimally install the package including
its `manyio` extra like `cratedb-about[manyio]`. After opting in, you can address
resources on many filesystems through the excellent [filesystem-spec] package.
Alternatively to the `--url` option, you can also use the `ABOUT_OUTLINE_URL`
environment variable.

#### API
Use the Python API to retrieve individual sets of outline items, for example,
by section name. The standard section names are: Docs, API, Examples, Optional.
```python
from cratedb_about import CrateDbKnowledgeOutline

# Load information from the built-in YAML file.
outline = CrateDbKnowledgeOutline.load()

# Load information from a remote YAML file.
# outline = CrateDbKnowledgeOutline.load("http://example.org/outline.yaml")

# List available section names.
outline.get_section_names()

# Retrieve information about resources from the "Docs" and "Examples" sections.
outline.find_items(section_name="Docs").to_list()
outline.find_items(section_name="Examples").to_list()

# Convert outline into Markdown format.
outline.to_markdown()

# Convert outline into llms-txt format (medium).
outline.to_llms_txt()

# Convert outline into llms-txt format (full).
outline.to_llms_txt(optional=True)
```

### Bundle
The Markdown file `outline.md` serves as the source for producing the
`llms.txt` files. Generate multiple `llms.txt` files along with any
auxiliary output files.
```shell
cratedb-about bundle --format=llm --outdir=./public_html
```
By default, the bundler will use the built-in `cratedb-outline.yaml` as input file.
You can select an alternative input file using the `--url` option, or the
`ABOUT_OUTLINE_URL` environment variable. The output directory can
also be specified using the `OUTDIR` environment variable.

### Query
Ask questions about CrateDB from the command line.
#### CLI
Execute a prompt using the built-in Python implementation.
```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
cratedb-about ask "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```
Hold an ongoing chat with a model using the versatile [`llm`] application.
```shell
uvx llm chat --model gpt-4.1 --option temperature 0.5 \
  --fragment https://cdn.crate.io/about/v1/llms-full.txt \
  --system-fragment https://cdn.crate.io/about/v1/instructions-general.md
```
If you are running out of questions, get inspired by the standard library.
```shell
cratedb-about list-questions
```
#### API
Use the built-in Python API to ask questions about CrateDB.
```python
from cratedb_about import CrateDbKnowledgeConversation

knowledge = CrateDbKnowledgeConversation()
knowledge.ask("CrateDB does not seem to provide an AUTOINCREMENT feature?")
```
Use the Python API of the `llm` package to ask questions about CrateDB.
```python
import llm

model = llm.get_model("gpt-4.1")
response = model.prompt(
    "CrateDB does not seem to provide an AUTOINCREMENT feature?",
    fragments=["https://cdn.crate.io/about/v1/llms-full.txt"],
    system_fragments=["https://cdn.crate.io/about/v1/instructions-general.md"],
    temperature=0.5,
)
print(response.text())
```
#### Notes
- To configure a different context file, use the `ABOUT_CONTEXT_URL`
  environment variable. It can be a remote URL or a path on the local filesystem.
  The default value is <https://cdn.crate.io/about/v1/llms-full.txt>.
- Remote resources will be cached for one hour (3600 seconds) to strike the
  balance between freshness and resource saving. Use the `ABOUT_CACHE_TTL`
  environment variable to reconfigure that value in seconds.

## FAQ

- Q: Seriously, how do I use this?

  A: As mentioned above, this repository includes content and a few utilities
  to manage corresponding information. Users will directly use the produced
  [llms.txt] and [llms-full.txt] files. Developers will install the [cratedb-about]
  package to access fundamental outline information in their own programs
  programmatically, or to invoke fragments of the production machinery
  on their premises, either ad hoc, or by including it in automated pipelines.

- Q: It looks like the knowledge base machinery is missing important information
  about CrateDB. I've asked it about matters of polymer sharding, and the answer
  wasn't very insightful.

  A: Well, we can understand your disappointment. To improve the situation,
  we are constantly curating content, and you can support the process by giving
  us hints about which fragments of information to include in the set of
  curated information. To learn about what this means, see also [ABOUT-24].

## Project Information

### Acknowledgements
Kudos to the authors of all the many software components and technologies
this project is building upon.

### Contributing
The `cratedb-about` package is an open source project, and is [managed on
GitHub]. Contributions of any kind are welcome and appreciated.

### Status
The software is in the pre-alpha (planning) stage. Version pinning is strongly
recommended, especially if you use it as a library.


[ABOUT-24]: https://github.com/crate/about/issues/24
[about/v1]: https://cdn.crate.io/about/v1/
[CrateDB]: https://cratedb.com/database
[cratedb-about]: https://pypi.org/project/cratedb-about/
[instructions.md]: https://github.com/crate/about/blob/main/src/cratedb_about/prompt/instructions.md
[cratedb-mcp]: https://github.com/crate/cratedb-mcp
[cratedb-outline.yaml]: https://github.com/crate/about/blob/main/src/cratedb_about/outline/cratedb-outline.yaml
[filesystem-spec]: https://filesystem-spec.readthedocs.io/
[hierarchical outline]: https://en.wikipedia.org/wiki/Outline_(list)
[`llm`]: https://llm.datasette.io/
[llms-txt]: https://llmstxt.org/
[llms.txt]: https://cdn.crate.io/about/v1/llms.txt
[llms-full.txt]: https://cdn.crate.io/about/v1/llms-full.txt
[Markdown]: https://daringfireball.net/projects/markdown/
[Model Context Protocol (MCP)]: https://modelcontextprotocol.io/introduction
[uv]: https://docs.astral.sh/uv/
[YAML]: https://en.wikipedia.org/wiki/Yaml

[Bluesky]: https://bsky.app/search?q=cratedb
[Community Forum]: https://community.cratedb.com/
[Documentation]: https://github.com/crate/about
[Issues]: https://github.com/crate/about/issues
[License]: https://github.com/crate/about/blob/main/LICENSE
[managed on GitHub]: https://github.com/crate/about
[Source code]: https://github.com/crate/about
[Releases]: https://github.com/crate/about/releases

[badge-ci]: https://github.com/crate/about/actions/workflows/tests.yml/badge.svg
[badge-coverage]: https://codecov.io/gh/crate/about/branch/main/graph/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/cratedb-about/month
[badge-license]: https://img.shields.io/github/license/crate/about.svg
[badge-package-version]: https://img.shields.io/pypi/v/cratedb-about.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/cratedb-about.svg
[badge-release-notes]: https://img.shields.io/github/release/crate/about?label=Release+Notes
[badge-status]: https://img.shields.io/pypi/status/cratedb-about.svg
[project-ci]: https://github.com/crate/about/actions/workflows/tests.yml
[project-coverage]: https://app.codecov.io/gh/crate/about
[project-downloads]: https://pepy.tech/project/cratedb-about/
[project-github]: https://github.com/crate/about
[project-license]: https://github.com/crate/about/blob/main/LICENSE
[project-pypi]: https://pypi.org/project/cratedb-about
[project-release-notes]: https://github.com/crate/about/releases
