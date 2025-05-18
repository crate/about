# Backlog

## Iteration +1
- Bundle: Compare sizes of CrateDB's `llms.txt` files against sizes
  of other vendors. Adjust when needed.
  https://github.com/crate/about/issues/20
- Bundle: `test_cli_bundle` is heavy, and may incur timeouts
- Linter: YAML, Markdown, Linkchecker, Element sizes

## Iteration +2
- UI: Little chat interface using Streamlit
- Any: JSON/YAML/Markdown output
- Query: Let the user optionally select a local or remote `llms.txt` file
- Query: Let the user select the model, reasoning effort, and other parameters
- Outline: `find_items`: Include and/or exclude multiple sections
- Outline: Refactor `--optional` flag to `--include=optional` option
- Bundle: Don't let HTML leak into bundle files

## Iteration +3
- Bundle: Explore using refined content representations by
  pulling in `ctk docs functions` and `ctk docs settings`
- Outline: Unlock Discourse, auto-select https://community.cratedb.com/raw/1015
- Outline: Unlock HTML resources, auto-convert using the best standalone program.
  => https://www.urltoany.com/url-to-markdown
- Outline: Unlock GitHub projects: https://github.com/mattduck/gh2md

## Done
- Package: Publish to PyPI
- Outline: `load`: Load from custom outline file
- Outline: Refactor `llm_txt2ctx` shell-outs to API, and add to `outline` subcommand
- Outline: Refactor ingredients of `build` subcommand
- llms-txt: Rename subcommand `build` to `bundle --format=llms-txt`
- Outline: Refactor quirky `as_dict` parameter to more fluent `.to_dict()` interface
- Outline: Improve interface of `CrateDbKnowledgeOutline`: read() vs. load()
  => Better provide a context manager interface right away?
- Outline: Rename `CRATEDB_CONTEXT_URL` to `ABOUT_CONTEXT_URL`
- Outline: Rename `OUTLINE_URL` to `ABOUT_OUTLINE_URL`
- Outline: Is the built-in outline currently validated?
- Bundle: README in HTML format
- Inventory: Revisit `notes` in `cratedb-outline.yaml` about
  other resources that have not been expanded properly yet
  https://github.com/crate/about/issues/24
- Inventory: Information about ddl/views, etc., `COPY FROM ...`,
  and `ctk load table`, specifically about how to load data and import demo data
