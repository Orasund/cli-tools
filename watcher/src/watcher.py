import os 
import click
import hashlib
import time

@click.command()
@click.argument("path")
@click.argument("callback")
def watcher(path,callback):
    """watch the PATH and call CALLBACK if the content changes"""
    mtime = os.stat(path).st_mtime
    mtime_new = os.stat(path).st_mtime
    while (mtime != mtime_new):
        mtime = mtime_new
        time.sleep(1)
        mtime_new = os.stat(path).st_mtime
    os.system(callback)
        

if __name__ == '__main__':
    watcher()