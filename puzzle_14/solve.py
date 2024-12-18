import utils.utils as utils
import time

fileName = "puzzle_14/input.txt"


def solve():
    print("Solving puzzle 14 of Advent of Code 2024")
    robots = utils.readFileLines(fileName)
    robots = [getRobot(robotStr) for robotStr in robots]
    move(robots,100)
    print(getSafetyFactor(robots))
    
    robots = utils.readFileLines(fileName)
    robots = [getRobot(robotStr) for robotStr in robots]
    index=7268
    move(robots,7268)
    # every 101, loops on vertical drawing, starting at 99
    # every 103, loops on horizontal drawing starting at 58
    # prints when both match
    while index<7371:
        index+=103
        move(robots,103)
        print(index)
        printRobots(robots)
        time.sleep(0.05)

def getRobot(robotStr):
    pos,velocity = robotStr.split(" v=")
    x,y = pos.replace("p=","").split(",")
    vx,vy = velocity.split(",")
    return list(map(int,[x,y,vx,vy]))

def move(robots,time):
    maxX, maxY= 101, 103
    for robot in robots:
        x,y,vx,vy = robot
        x = (x+vx*time) %maxX
        y = (y+vy*time) %maxY
        robot[0] = x
        robot[1] = y

def getSafetyFactor(robots):
    middleX = 50 # 0 to 49 then 51 to 100
    middleY = 51 # 0 to 50 then 52 to 102
    q1,q2,q3,q4=0,0,0,0
    for x,y,vx,vy in robots:
        if x < middleX:
            if y< middleY:
                q1+=1
            elif y> middleY:
                q2+=1
        elif x > middleX:
            if y< middleY:
                q3+=1
            elif y> middleY:
                q4+=1
    return q1*q2*q3*q4

def printRobots(robots):
    grid = getGrid(101,103)
    for x,y,vx,vy in robots:
        grid[y][x]+=1
    gridStr = [[printRobotNb(pos) for pos in line] for line in grid]
    utils.printColoredMap(gridStr)

def printRobotNb(pos):
    if pos == 0: return " "
    else: return str(pos)

def getGrid(x, y):
    return [[0 for i in range(x)] for j in range(y)]