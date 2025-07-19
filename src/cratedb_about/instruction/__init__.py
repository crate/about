import importlib.resources

instructions_file = (
    importlib.resources.files("cratedb_about.instruction") / "cratedb-instructions.md"
)
instructions_text = instructions_file.read_text()


class Instructions:
    """
    Bundle a few general instructions how to work with CrateDB.

    - Introduction: https://github.com/crate/about/blob/main/src/cratedb_about/outline/cratedb-outline.yaml#L27-L40
    - General notes about writing principles: https://github.com/jlowin/fastmcp/blob/main/docs/.cursor/rules/mintlify.mdc#L10-L34
    """

    @classmethod
    def full(cls) -> str:
        return instructions_text
