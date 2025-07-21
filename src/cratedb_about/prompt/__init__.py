import importlib.resources


class GeneralInstructions:
    """
    Bundle a few general instructions about how to work with CrateDB.

    - Things to remember when working with CrateDB: https://github.com/crate/about/blob/main/src/cratedb_about/outline/cratedb-outline.yaml#L27-L40
    - Impersonation, Rules for writing SQL queries: https://github.com/crate/cratedb-examples/blob/7f1bc0f94/topic/chatbot/table-augmented-generation/aws/cratedb_tag_inline_agent.ipynb?short_path=00988ad#L777-L794
    - Key guidelines: Thanks, @WalBeh.
    - Core writing principles: https://github.com/jlowin/fastmcp/blob/main/docs/.cursor/rules/mintlify.mdc#L10-L34. Thanks, @jlowin.
    """  # noqa: E501

    def __init__(self):
        instructions_file = importlib.resources.files("cratedb_about.prompt") / "instructions.md"
        self.instructions_text = instructions_file.read_text()

    def render(self) -> str:
        return self.instructions_text
