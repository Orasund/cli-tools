from click.testing import CliRunner
from src.diff_files import diff_files


def test_empty():
    runner = CliRunner()
    result = runner.invoke(diff_files, ["tests/data/empty", "tests/data/empty"])
    assert result.exit_code == 0
    assert result.output == "[([], [])]\n"


def test_basic():
    runner = CliRunner()
    result = runner.invoke(diff_files, ["tests/data/file1", "tests/data/file2"])
    expected = ("["
                "(['Hello \\n'], []), "
                "(['beautiful\\n'], "
                "['little\\n', 'boy\\n', 'lives\\n', 'in\\n', 'his\\n', 'own\\n']), "
                "(['\\n'], ['!'])"
                "]\n")
    assert result.output == expected
