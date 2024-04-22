import os

from click.testing import CliRunner
from diff_files import diff_files, build_subsequence_matrix, compute_common_indices, compute_differences


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


def test_diff():
    os.chdir(os.path.dirname(__file__))
    with open("data/file1") as f1, open("data/file2") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    matrix = build_subsequence_matrix(lines1, lines2)
    # 2. Walk the graph and collect all the indecies where the strings match
    common_indices = compute_common_indices(matrix)
    # 3. Compute the differences based on the collected indecies
    differences = compute_differences(lines1, lines2, common_indices)
    assert differences == [
        (['Hello \n'], []),
        (['beautiful\n'], ['little\n', 'boy\n', 'lives\n', 'in\n', 'his\n', 'own\n']),
        (['\n'], ['!'])]
