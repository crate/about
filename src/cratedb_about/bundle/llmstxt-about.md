# CrateDB's llms.txt

## Introduction

[llms.txt] is a proposal to standardise on using an `/llms.txt` file to provide
information to help LLMs use a website at inference time. It is designed to
coexist with current web standards.

While sitemaps list all pages for search engines, llms.txt offers a curated
overview for LLMs. It can complement robots.txt by providing context for allowed
content. The file can also reference structured data markup used on the site,
helping LLMs understand how to interpret this information in context.

## What's Inside

- `cratedb-outline.yaml`: The YAML source file for generating a Markdown file
  `cratedb-outline.md` and subsequently an `llms.txt`.
- `llms.txt`: Standard `llms.txt` file.
- `llms-full.txt`: Full `llms.txt` file, including the "Optional" subsection.


[llms.txt]: https://llmstxt.org/
