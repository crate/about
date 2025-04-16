# Sandbox

Acquire the source code repository.
```shell
git clone https://github.com/crate/about cratedb-about
cd cratedb-about
```

Rebuild all the `llms.txt` files.
```shell
uv run poe build
```

Ask questions about CrateDB.
```shell
uvx --with-editable=. cratedb-about ask "CrateDB does not seem to provide an AUTOINCREMENT feature?"
```

If you are running out of questions, get inspired by the standard library.
```shell
uvx --with-editable=. cratedb-about list-questions
```
