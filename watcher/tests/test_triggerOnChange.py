from click.testing import CliRunner
from src.watcher import watcher
import os
import io
import time

def test():
  path = "tests/folder/"
  file = "test_file"
  file_success = "success"
  cmd = "echo 'works' > " + path + file_success
 

  runner = CliRunner()
  io.open(path + file,"x")
  result = runner.invoke(watcher, [path,cmd])
  os.remove(path + file)
  time.sleep(1)
  exists = os.path.exists(path + file_success)
  os.remove(path + file_success)
  
  assert result.exit_code == 0
  assert exists 