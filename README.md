# About CrateDB

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

Install `cratedb-about` package.
```shell
uv tool install --upgrade 'cratedb-about[all] @ git+https://github.com/crate/about'
```

## Usage

### Outline

#### CLI
Convert documentation outline from `cratedb-outline.yaml` into Markdown format,
which is the source file for subsequently expanding it into an `llms.txt` file.
```shell
cratedb-about outline --format=markdown > outline.md
llms_txt2ctx --optional=true outline.md > llms-full.txt
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

# Retrieve information about resources from the "Docs" and "Examples" sections.
doc_items = outline.get_items("Docs", as_dict=True)
example_items = outline.get_items("Examples", as_dict=True)

# List available section names.
section_names = outline.section_names
```

### llms-txt

#### Build

Rebuild all `llms.txt` and auxiliary files.
```shell
export OUTDIR=./public_html
cratedb-about build
```

#### Query

Ask questions about CrateDB.
```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
cratedb-about ask "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```

If you are running out of questions, get inspired by the standard library.
```shell
cratedb-about list-questions
```

To configure a different context file, use the `CRATEDB_CONTEXT_URL` environment
variable. The default value is https://cdn.crate.io/about/v1/llms-full.txt.


[about/v1]: https://cdn.crate.io/about/v1/
[CrateDB]: https://cratedb.com/database
[cratedb-mcp]: https://github.com/crate/cratedb-mcp
[cratedb-outline.yaml]: https://github.com/crate/about/blob/main/src/cratedb_about/outline/cratedb-outline.yaml
[llms.txt]: https://llmstxt.org/
[Model Context Protocol (MCP)]: https://modelcontextprotocol.io/introduction
