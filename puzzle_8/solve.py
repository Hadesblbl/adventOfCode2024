import utils.utils as utils

fileName = "puzzle_8/input.txt"

def solve():
    print("Solving puzzle 8 of Advent of Code 2024")
    lines = utils.readFileLines(fileName)
    pos=getPositions(lines)
    maxX,maxY = len(lines[0]), len(lines)
    
    posAntiNodes = getPosAntinodes(pos,maxX,maxY)
    #lines = fillLinesWithPositions(list(map(list,lines)),posAntiNodes)
    #utils.printColoredMap(lines)
    print(len(posAntiNodes))
    posAntiNodes = getPosAntinodes2(pos,maxX,maxY)
    print(len(posAntiNodes))

def getPositions(grid):
    pos={}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = grid[y][x]
            if c == ".":
                continue
            if c in pos:
                pos[c].append([x,y])
            else:
                pos[c] = [[x,y]]
    return pos

def getPosAntinodes(positions,maxX,maxY):
    antinodes=set({})
    for c in positions:
        nbPositions = len(positions[c])
        # tous les couples même fréquence
        for i in range(nbPositions):
            for j in range(i+1,nbPositions):
                x1,y1 = positions[c][i]
                x2,y2 = positions[c][j]
                
                dx,dy=x1-x2,y1-y2
                # antinodes
                a1x,a1y = x1+dx, y1+dy
                if isValid(a1x,a1y,maxX,maxY):
                    antinodes.add(getPos(a1x,a1y))
                a2x,a2y = x2-dx, y2-dy
                if isValid(a2x,a2y,maxX,maxY):
                    antinodes.add(getPos(a2x,a2y))
    return antinodes

def getPosAntinodes2(positions,maxX,maxY):
    antinodes=set({})
    for c in positions:
        nbPositions = len(positions[c])
        # tous les couples même fréquence
        for i in range(nbPositions):
            for j in range(i+1,nbPositions):
                x1,y1 = positions[c][i]
                x2,y2 = positions[c][j]
                
                dx,dy=x1-x2,y1-y2
                
                a1x,a1y = x1, y1
                a2x,a2y = x2, y2
                while(isValid(a1x,a1y,maxX,maxY)):
                    antinodes.add(getPos(a1x,a1y))
                    a1x+=dx
                    a1y+=dy
                while(isValid(a2x,a2y,maxX,maxY)):
                    antinodes.add(getPos(a2x,a2y))
                    a2x-=dx
                    a2y-=dy
    return antinodes

def isValid(x,y,maxX,maxY):
    return x>=0 and y >= 0 and x < maxX and y < maxY

def getPos(x,y):
    return str(x)+":"+str(y)

def getXY(pos):
    return list(map(int,pos.split(":")))

def fillLinesWithPositions(lines,positions):
    for position in positions:
        x,y=getXY(position)
        lines[y][x] = "#"
    return lines
        