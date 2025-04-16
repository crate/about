# About CrateDB

A high-level description about [CrateDB], with cross-references
to relevant resources in the spirit of a curated knowledge backbone.

> CrateDB is a distributed and scalable SQL database for storing and
> analyzing massive amounts of data in near real-time, even with
> complex queries. It is based on Lucene, inherits technologies from
> Elasticsearch, and is compatible with PostgreSQL.

## What's inside

- The [cratedb-overview.md] file includes hints about what CrateDB is
  and what you can do with it.

- The [build/llm] folder includes a few [llms.txt] files generated from
  [cratedb-overview.md]. They can be used to provide better context
  for conversations about CrateDB.

## Usage

Install `cratedb-about` package.
```shell
uv tool install --upgrade 'cratedb-about @ git+https://github.com/crate/about'
```

Ask questions about CrateDB.
```shell
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
cratedb-about ask "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```

If you are running out of questions, get inspired by the standard library.
```shell
cratedb-about list-questions
```


[build/llm]: ./build/llm
[CrateDB]: https://cratedb.com/database
[cratedb-overview.md]: ./src/index/cratedb-overview.md
[llms.txt]: https://llmstxt.org/
