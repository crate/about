# About CrateDB changelog

## Unreleased
- Chore: Removed `sponge` command in `poe build`
- Content: Added two pieces of content from blog articles, converted to Markdown format
- Documentation: Started advertising to use the designated location
  https://cdn.crate.io/about/ for consuming the generated resources
- Naming things: Adhered to the naming convention of [LLMs.txt Hub]
  by using `llms.txt` and `llms-full.txt`.

## v0.0.1 - 2025-04-17
- Established project layout
- Added source files (`cratedb-overview.md`), generator program wrapper
  (`uv run poe build`), and build artifacts (`llms-ctx.txt` and `llms-ctx-full.txt`)
- Added CLI program `cratedb-about` with subcommands `ask` and `list-questions`
  for ad hoc conversations about CrateDB


[LLMs.txt Hub]: https://llmtxt.dev/hub
