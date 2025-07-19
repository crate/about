from cratedb_about.instruction import Instructions


def test_instructions_full():
    instructions_text = Instructions.full()
    assert "Things to remember when working with CrateDB" in instructions_text
    assert "Rules for writing SQL queries" in instructions_text
    assert "Core writing principles" in instructions_text
