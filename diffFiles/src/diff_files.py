from dataclasses import dataclass
from typing import cast, IO
import click


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Node:
    next_pos: Position
    length: int


@dataclass
class Matrix:
    nodes: list[list[Node]]

    def get_node(self, pos: Position) -> Node | None:
        if pos.x < 0 or pos.y < 0:
            return None
        return self.nodes[pos.x][pos.y]

    @classmethod
    def make(cls, l1: list[str], l2: list[str]) -> "Matrix":
        def compute_node(i1: int, i2: int, line1, line2) -> Node:
            next_pos: Position | None
            length: int

            if line1 == line2:
                next_pos = Position(i1 - 1, i2 - 1)
                length = result.nodes[next_pos.x][next_pos.y].length + 1
            else:
                candidate1 = Position(i1, i2 - 1)
                candidate2 = Position(i1 - 1, i2)
                node1 = result.get_node(candidate1)
                node2 = result.get_node(candidate2)

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

        result = Matrix([])
        for i1, line1 in enumerate(l1):
            result.nodes.append([])
            for i2, line2 in enumerate(l2):
                result.nodes[i1].append(compute_node(i1, i2, line1, line2))
        return result


def build_subsequence_matrix(l1: list[str], l2: list[str]) -> Matrix:
    # we use the matrix as a graph
    # where each node points to one of their neighbors
    nodes = Matrix.make(l1, l2)
    return nodes


def compute_common_indices(nodes: Matrix) -> list[Position]:
    common_indices: list[Position] = []
    if not nodes.nodes:
        return common_indices

    pos = Position(len(nodes.nodes) - 1, len(nodes.nodes[0]) - 1)

    def get_node(p: Position) -> Node:
        result = nodes.get_node(p)
        if result is None:
            return Node(Position(0, 0), 0)
        return result

    node: Node = get_node(pos)

    while node.next_pos is not None:
        next_node = get_node(node.next_pos)

        if next_node.length < node.length:
            common_indices.append(pos)

        pos = node.next_pos
        node = next_node

    common_indices.reverse()
    return common_indices


def compute_differences(
        lines1: list[str], lines2: list[str], commons_indices: list[Position]
):
    indices: list[Position] = (
            [Position(-1, -1)] + commons_indices + [Position(len(lines1), len(lines2))]
    )

    return [
        (lines1[iMin.x + 1: iMax.x], lines2[iMin.y + 1: iMax.y])
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
    common_indices = compute_common_indices(matrix)
    # 3. Compute the differences based on the collected indecies
    differences = compute_differences(lines1, lines2, common_indices)

    click.echo(differences)


if __name__ == "__main__":
    diff_files()
