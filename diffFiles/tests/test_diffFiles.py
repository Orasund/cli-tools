from click.testing import CliRunner
from diffFiles.src.diff_files import diff_files


def test():
    runner = CliRunner()
    result = runner.invoke(diff_files, ["tests/data/file1", "tests/data/file2"])
    expected = "[(['Hello \\n'], []), (['beautiful\\n'], ['little\\n', 'boy\\n', 'lives\\n', 'in\\n', 'his\\n', 'own\\n']), (['\\n'], ['!'])]\n"
    assert result.output == expected
