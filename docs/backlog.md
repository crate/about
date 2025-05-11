# Backlog

## Iteration +1
- Outline: Refactor `llm_txt2ctx` shell-outs to API, and add to `outline` subcommand
- Outline: Refactor ingredients of `build` subcommand
- Outline: Refactor quirky `as_dict` parameter to more fluent `.to_dict()` interface
- Outline: Revisit `notes` in `cratedb-outline.yaml`, for example about
  pulling in `ctk docs functions` and `ctk docs settings`, but also about
  other resources that have not been expanded properly yet
- Outline: Rename `CRATEDB_CONTEXT_URL` to `ABOUT_CONTEXT_URL`
- Outline: Rename `OUTLINE_URL` to `ABOUT_OUTLINE_URL`
- Outline: Improve interface of `CrateDbKnowledgeOutline`: read() vs. load()
  => Better provide a context manager interface?
- llms-txt: Rename subcommand `build` to `llms-txt build`

## Iteration +2
- Any: JSON/YAML/Markdown output
- Query: Let the user optionally select a local or remote `llms.txt` file
- Query: Let the user select the model, reasoning effort, and other parameters
- Outline: `find_items`: Include and/or exclude multiple sections

## Iteration +3
- Outline: Unlock Discourse, auto-select https://community.cratedb.com/raw/1015
- Outline: Unlock HTML resources, auto-convert using the best standalone program.
  => https://www.urltoany.com/url-to-markdown
- Outline: Unlock GitHub projects: https://github.com/mattduck/gh2md

## Done
- Package: Publish to PyPI
- Outline: `load`: Load from custom outline file
