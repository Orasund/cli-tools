from click.testing import CliRunner
from src.hashFile import hashFile

def test():
  runner = CliRunner()
  result = runner.invoke(hashFile, ['tests/trivial/input'])
  assert result.output == open('tests/trivial/output', "r").read() + "\n"