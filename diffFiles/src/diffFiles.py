import click
import hashlib

# https://en.wikipedia.org/wiki/Longest_common_subsequence

class Node:
    def __init__(self,nextPos:tuple[int,int] | None,length:int) -> None:
        self.nextPos = nextPos 
        self.length = length

def buildMatrix(l1:list[str],l2:list[str]) -> list[list[Node]]:
    nodes:list[list[Node]] = []

    def getNode(pos:tuple[int,int]) -> Node | None:
        return nodes[pos[0]][pos[1]] if pos[0] >= 0 and pos[1] >= 0 else None

    def computeNode(i1:int,i2:int) -> Node:
        nextPos:tuple[int,int] | None
        length:int

        if (l1[i1] == l2[i2]):
                nextPos = (i1-1,i2-1)
                length = nodes[nextPos[0]][nextPos[1]].length + 1
        else: 
            candidate1 = (i1,i2-1)
            candidate2 = (i1-1,i2)
            node1 = getNode(candidate1)
            node2 = getNode(candidate2)

            #find the candidate with the bigger length
            if node1 == None and node2 == None:
                    nextPos = None
                    length = 0
            elif node1 == None or (node2 != None and node1.length < node2.length):
                    nextPos = candidate2
                    length = node2.length
            else:
                    nextPos = candidate1
                    length = node1.length
                
        return Node(nextPos,length)


    for i1 in range(len(l1)):
        nodes.append([])
        for i2 in range(len(l2)):
            nodes[i1].append(computeNode(i1,i2))
    return nodes

def computeCommonIndices(nodes:list[list[Node]]) -> list[tuple[int,int]]:
    pos:tuple[int,int] = (len(nodes)-1,len(nodes[0])-1)

    def getNode(pos:tuple[int,int]) -> Node:
        return nodes[pos[0]][pos[1]]

    node:Node = getNode(pos)
    commonIndices:list[tuple[int,int]] = []
    
    while node.nextPos != None:
        nextNode = getNode(node.nextPos)
        
        if nextNode.length < node.length:
            commonIndices.append(pos)

        pos = node.nextPos
        node = nextNode

    commonIndices.reverse()
    return commonIndices

def computeDifferences(lines1:list[str],lines2:list[str],commonsIndices:list[tuple[int,int]]):
    indices:list[tuple[int,int]] = [(-1,-1)] + commonsIndices + [(len(lines1),len(lines2))]
    
    return [(lines1[iMin[0]+1:iMax[0]],lines2[iMin[1]+1:iMax[1]]) for (iMin,iMax) in zip(indices,indices[1:])]

@click.command()
@click.argument("file1")
@click.argument("file2")
def diffFiles(file1:click.Path,file2:click.Path):
    """Return the difference between FILE1 and FILE2"""
    lines1:list[str] = open(file1, "r").readlines()
    lines2:list[str] = open(file2, "r").readlines()
    
    matrix = buildMatrix(lines1,lines2)
    commonIndices = computeCommonIndices(matrix)
    differences = computeDifferences(lines1,lines2,commonIndices)


    click.echo(differences)

if __name__ == '__main__':
    diffFiles()