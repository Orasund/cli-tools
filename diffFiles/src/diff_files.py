from typing import cast, IO
import click


class Node:
    def __init__(self, next_pos: tuple[int, int] | None, length: int) -> None:
        self.next_pos = next_pos
        self.length = length


def build_subsequence_matrix(l1: list[str], l2: list[str]) -> list[list[Node]]:
    # we use the matrix as a graph
    # where each node points to one of their neighbors
    nodes: list[list[Node]] = []

    def get_node(pos: tuple[int, int]) -> Node | None:
        return nodes[pos[0]][pos[1]] if pos[0] >= 0 and pos[1] >= 0 else None

    def compute_node(i1: int, i2: int) -> Node:
        next_pos: tuple[int, int] | None
        length: int

        if l1[i1] == l2[i2]:
            next_pos = (i1 - 1, i2 - 1)
            length = nodes[next_pos[0]][next_pos[1]].length + 1
        else:
            candidate1 = (i1, i2 - 1)
            candidate2 = (i1 - 1, i2)
            node1 = get_node(candidate1)
            node2 = get_node(candidate2)

            # find the candidate with the bigger length
            if node1 is None and node2 is None:
                next_pos = None
                length = 0
            elif node2 is not None and (node1 is None or node1.length < node2.length):
                next_pos = candidate2
                length = node2.length
            else:
                next_pos = candidate1
                length = cast(Node, node1).length

        return Node(next_pos, length)

    for i1 in range(len(l1)):
        nodes.append([])
        for i2 in range(len(l2)):
            nodes[i1].append(compute_node(i1, i2))
    return nodes


def compute_common_indices(nodes: list[list[Node]]) -> list[tuple[int, int]]:
    commonIndices: list[tuple[int, int]] = []
    if not nodes:
        return commonIndices

    pos: tuple[int, int] = (len(nodes) - 1, len(nodes[0]) - 1)

    def get_node(pos: tuple[int, int]) -> Node:
        return nodes[pos[0]][pos[1]]

    node: Node = get_node(pos)

    while node.next_pos is not None:
        nextNode = get_node(node.next_pos)

        if nextNode.length < node.length:
            commonIndices.append(pos)

        pos = node.next_pos
        node = nextNode

    commonIndices.reverse()
    return commonIndices


def compute_differences(
    lines1: list[str], lines2: list[str], commonsIndices: list[tuple[int, int]]
):
    indices: list[tuple[int, int]] = (
        [(-1, -1)] + commonsIndices + [(len(lines1), len(lines2))]
    )

    return [
        (lines1[iMin[0] + 1 : iMax[0]], lines2[iMin[1] + 1 : iMax[1]])
        for (iMin, iMax) in zip(indices, indices[1:])
    ]


@click.command()
@click.argument("file1", type=click.File(mode="r"))
@click.argument("file2", type=click.File(mode="r"))
def diff_files(file1: IO, file2: IO):
    """Return the difference between FILE1 and FILE2"""
    lines1: list[str] = file1.readlines()
    lines2: list[str] = file2.readlines()

    # Algorithm taken from
    # https://en.wikipedia.org/wiki/Longest_common_subsequence
    #
    # 1. Build a graph of subsequences (stores as a matrix)
    matrix = build_subsequence_matrix(lines1, lines2)
    # 2. Walk the graph and collect all the indecies where the strings match
    commonIndices = compute_common_indices(matrix)
    # 3. Compute the differences based on the collected indecies
    differences = compute_differences(lines1, lines2, commonIndices)

    click.echo(differences)


if __name__ == "__main__":
    diff_files()
