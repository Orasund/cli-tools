# DiffFiles

## Installation

### During development
In `diffFiles/`:
```shell
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

This makes an editable installation. You can test it by running
```shell
diff-file --help
```

To build an installable wheel and package, make sure you have
`build` installed and run
```shell
python -m build
```
This will create `dist/` with `diff_files-0.1.tar.gz` and 
`diff_files-0.1-py3-none-any.whl` in it.

To pin your requirements, make sure you have `pip-tools` installed and call
```shell
pip-compile -o requirements.txt pyproject.toml
```
This will update `requirements.txt` with the latest pinned versions.

### In "production"
The wheel and package can be installed on any computer, e.g. with
```shell
python -m pip install diff_files-0.1.tar.gz
```

## Run
An installation provides run-able executables in `venv/bin` (on Windows: `venv/Scripts`).

The main entry-point is `diff-file`, so you can use it like this:
```shell
diff-file FILE1 FILE2
```

## Test

In diffFiles-folder, run

```
pytest
```