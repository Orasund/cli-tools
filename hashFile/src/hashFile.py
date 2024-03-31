from io import BufferedReader
import click
import hashlib

@click.command()
@click.argument("filepath")
def hashFile(filepath:click.File):
    """Hash the content of the file"""
    f = open(filepath, "rb").read()
    hash = hashlib.sha256(f).hexdigest()
    click.echo(hash)

if __name__ == '__main__':
    hashFile()