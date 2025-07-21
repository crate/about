from cratedb_about.instruction import GeneralInstructions


def test_instructions_full():
    instructions_text = GeneralInstructions().render()
    assert "Things to remember when working with CrateDB" in instructions_text
    assert "Rules for writing SQL queries" in instructions_text
    assert "Core writing principles" in instructions_text
