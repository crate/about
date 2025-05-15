# About CrateDB changelog

## Unreleased
- Outline: `cratedb-about outline` now understands `--url` option to use
  any outline resource on local or remote filesystems. Alternatively, use
  the `ABOUT_OUTLINE_URL` environment variable.
- Outline: Added `to_llms_txt` API method and CLI options `--format=llms-txt`
  and `--optional`, to directly convert/expand the source outline file into
  an `llms.txt` file.
- llms-txt: Renamed subcommand `build` to `bundle --format=llms-txt`
- Outline: Refactored quirky `as_dict` parameter to more fluent `.to_dict()`
  interface
- Query: Added a few example questions specific to CrateDB
- Outline: Renamed `CRATEDB_CONTEXT_URL` to `ABOUT_CONTEXT_URL`
- Outline: Fixed `llms_txt` currently does not accept newlines in description fields
- Outline: Significantly update `cratedb-outline.yaml`
- Bundle: Started accepting `--url`/`ABOUT_OUTLINE_URL` option to specify
  alternative input outline file
- Bundle: Improved handling of `--format` option
- Query: Permitted loading context file from local filesystem
  per `ABOUT_CONTEXT_URL`
- Query: Introduced caching for context payloads on HTTP remote URLs

## v0.0.3 - 2025-05-10
- Outline: Refactored the source of truth for the documentation outline
  into the package itself, and changed the format from Markdown to YAML,
  i.e. from `cratedb-overview.md` to `cratedb-outline.yaml`
- Outline: Provided new CLI subcommand `cratedb-about outline`
- Outline: Provided `cratedb_about.CrateDbKnowledgeOutline` API for retrieving
  information from the knowledge base outline within Python programs
- Context: Zapped working tree building by establishing the
  `cratedb-about bundle` subcommand
- CI: Added GHA workflow for publishing package to PyPI
- Outline: Improved data model and interface
- Query: Refactored LLM conversations code to `CrateDbKnowledgeConversation`

## v0.0.2 - 2025-05-09
- Content: Added two pieces of content from blog articles, converted to Markdown format
- Context: Started advertising to use the designated location
  https://cdn.crate.io/about/ for consuming the generated resources
- Context: Naming things: Adhered to the naming convention of [LLMs.txt Hub]
  by using `llms.txt` and `llms-full.txt`.
- Outline: Added the [CrateDB README]

## v0.0.1 - 2025-04-17
- Start: Established project layout
- Context: Added source files (`cratedb-overview.md`), generator program wrapper
  (`uv run poe build`), and build artifacts (`llms-ctx.txt` and `llms-ctx-full.txt`)
- Query: Added CLI program `cratedb-about` with subcommands `ask` and `list-questions`
  for ad hoc conversations about CrateDB


[CrateDB README]: https://github.com/crate/crate/blob/master/README.rst
[LLMs.txt Hub]: https://llmtxt.dev/hub
