import utils.utils as utils
from collections import deque

fileName = "puzzle_20/input.txt"


def solve():
    print("Solving puzzle 20 of Advent of Code 2024")
    maze = utils.readFileLines(fileName)
    maze = tuple([tuple(list(line)) for line in maze])
    # step 1, get all dists from every accessible empty spots, to the end
    distsToEnd = getDistsToEnd(maze)
    # step 2, use those dist to know and compare total time when finished cheating
    # Part 1
    print(getNbCheatingTime(maze, 2, distsToEnd))
    # Part 2
    print(getNbCheatingTime(maze, 20, distsToEnd))


def getDistsToEnd(maze):
    '''Returns dists of all accessible locations from end tile'''
    toVisit = deque()
    end = getPosEnd(maze, "E")
    toVisit.append(end)
    x, y, dist = end
    distsToEnd = {utils.getPos(x, y): dist}

    maxX = len(maze[0])
    maxY = len(maze)
    while len(toVisit) > 0:
        x, y, dist = toVisit.popleft()
        for nextx, nexty in utils.getAdjacent(x, y):
            if utils.outOfBounds(nextx, nexty, maxX, maxY) or maze[nexty][nextx] == "#" or utils.getPos(nextx, nexty) in distsToEnd:
                continue
            toVisit.append([nextx, nexty, dist+1])
            distsToEnd[utils.getPos(nextx, nexty)] = dist + 1
    return distsToEnd


def getNbCheatingTime(maze, maxTimeCheat, distsToEnd):
    '''Returns the number of different useful cheat possible dependening on the max distance to cheat'''
    minTimeAdvantage = 100
    toVisit = deque()
    toVisit.append(getPosStart(maze, "S"))
    maxX = len(maze[0])
    maxY = len(maze)
    cheats = set({})
    while len(toVisit) > 0:
        x, y, path = toVisit.popleft()
        pos = utils.getPos(x, y)
        distToEnd = distsToEnd[pos]
        # add all normal movements
        for nextX, nextY in utils.getAdjacent(x, y):
            if utils.outOfBounds(nextX, nextY, maxX, maxY) or maze[nextY][nextX] == "#" or utils.getPos(nextX, nextY) in path:
                continue
            newPath = set(path)
            newPath.add(utils.getPos(nextX, nextY))
            toVisit.append([nextX, nextY, newPath])
        # add all cheat possible from a path
        # check all y in bounds for maxTimeCheat
        for newy in range(max(y-maxTimeCheat, 0), min(y+maxTimeCheat+1, maxY)):
            dy = abs(newy-y)
            # check all x in bounds for maxTimeCheat, excluding what's already used for y
            for newx in range(max(x-(maxTimeCheat-dy), 0), min(x+maxTimeCheat+1-dy, maxX)):
                dx = abs(newx-x)
                newPos = utils.getPos(newx, newy)
                distTraveledWithCheat = dx+dy
                if maze[newy][newx] != "#" and newPos in distsToEnd and distsToEnd[newPos] - distToEnd >= distTraveledWithCheat + minTimeAdvantage:
                    cheats.add(getCheatPos(x, y, newx, newy))
    return len(cheats)


def getPosStart(maze, start):
    '''Pos = x, y, path'''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == start:
                return [j, i, set({})]
    return [-1, -1, set({})]


def getCheatPos(x, y, x2, y2):
    '''Returns a hashable position of cheat start and cheat end'''
    return tuple([x, y, x2, y2])


def getPosEnd(maze, end):
    '''Returns x, y, distToEnd for the end position in the maze'''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == end:
                return [j, i, 0]
    return [-1, -1, -1]
