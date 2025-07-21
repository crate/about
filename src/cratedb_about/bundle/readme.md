# CrateDB context knowledge

## About

A curated index of CrateDB documentation essentials.

Source: <https://github.com/crate/about>
<br>
Target: <https://cdn.crate.io/about/v1/>

## What's Inside

- `outline.yaml`: The YAML source file for generating the Markdown file.
- `outline.md`: The Markdown source file for generating the `llms.txt` file(s).
- `llms.txt`: Output file `llms.txt` (standard).
- `llms-full.txt`: Output file `llms.txt` (full), including the "Optional" section.
- `instructions.md`: Instructions to be used within system prompts to LLMs.

## Details

### llms-txt

[llms-txt] is a proposal to standardise on using an `/llms.txt` file to provide
information to help LLMs use a website at inference time. It is designed to
coexist with current web standards.
While sitemaps list all pages for search engines, llms.txt offers a curated
overview for LLMs. It can complement robots.txt by providing context for allowed
content. The file can also reference structured data markup used on the site,
helping LLMs understand how to interpret this information in context.



----
Updated on {host} at {timestamp}.


[llms-txt]: https://llmstxt.org/
