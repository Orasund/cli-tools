import os

from click.testing import CliRunner
from diff_files import diff_files


def test_empty():
    os.chdir(os.path.dirname(__file__))
    runner = CliRunner()
    result = runner.invoke(diff_files, ["data/empty", "data/empty"])
    assert result.exit_code == 0
    assert result.output == "[([], [])]\n"


def test_basic():
    os.chdir(os.path.dirname(__file__))
    runner = CliRunner()
    result = runner.invoke(diff_files, ["data/file1", "data/file2"])
    expected = ("["
                "(['Hello \\n'], []), "
                "(['beautiful\\n'], "
                "['little\\n', 'boy\\n', 'lives\\n', 'in\\n', 'his\\n', 'own\\n']), "
                "(['\\n'], ['!'])"
                "]\n")
    assert result.output == expected
