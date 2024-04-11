from click.testing import CliRunner
from src.diffFiles import diffFiles

def test():
  runner = CliRunner()
  result = runner.invoke(diffFiles, ["tests/data/file1","tests/data/file2"])
  expected = "[(['Hello \\n'], []), (['beautiful\\n'], ['little\\n', 'boy\\n', 'lives\\n', 'in\\n', 'his\\n', 'own\\n']), (['\\n'], ['!'])]\n"
  assert result.output == expected