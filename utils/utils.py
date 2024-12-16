import json

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

moves={"^":[0,-1],"v":[0,1],">":[1,0],"<":[-1,0]}

def readFile(fileName):
    with open(fileName) as file:
        result = file.read()
    return result

def readFileLines(fileName):
    with open(fileName) as file:
        lines = [line.rstrip("\n") for line in file.readlines()]
    return lines

def readGridOfChars(fileName):
    return list(map(list,readFileLines(fileName)))

def readLinesSeparatedByEmptyLines(fileName):
    lines = readFileLines(fileName)
    result=[]
    resultGroup=[]
    for line in lines:
        if(len(line) == 0):
            result.append(resultGroup)
            resultGroup=[]
        else:
            resultGroup.append(line)
    if(len(lines[len(lines)-1]) != 0):
        result.append(resultGroup)
    return result

def swap(l,i,j):
    l[i], l[j] = l[j], l[i]

def swapGrid(grid,x1,y1,x2,y2):
    grid[y1][x1], grid[y2][x2] = grid[y2][x2],grid[y1][x1]

#FIXME not the best
def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def getSum(numberList):
    listToSum = []
    if(isinstance(numberList[0], str)):
        listToSum = list(map(int, numberList))
    elif(isinstance(numberList[0], int)):
        listToSum = numberList
    return sum(listToSum)

def getMax(numberList):
    return max(numberList)

def getListOfNList(n):
    return [[] for i in range(n)]

def printMap(listOfList):
    for l in listOfList:
        print(l)

def printMapOfChars(listOfList):
    for l in listOfList:
        print("".join(l))

def getGrid(x,y):
    return [["" for i in range(x)] for j in range(y)]

def isAllDifferent(tab):
    seen = []
    for i in tab:
        if i in seen:
            return False
        else:
            seen.append(i)
    return True


def isMod2(x):
    unit = str(x)[-1]
    return int(unit)%2 == 0

def isMod3(x):
    if x == 3 or x==6 or x==9: return True
    if x<9 and x>-9: return False
    return isMod3(sum([int(number) for number in str(abs(x))]))

def isMod5(x):
    unit = str(x)[-1]
    return int(unit)%5 == 0

def isMod7(x):
    if(x<=56):
        return x%7 == 0
    number = str(abs(x))
    return isMod7(int(number[-1])*5 + int(number[:-1]))

def isMod11(x):
    number = str(abs(x))
    odd=0
    even=0
    for index in range(len(number)):
        if(index%2==0):
            odd+=int(number[index])
        else:
            even+=int(number[index])
    return abs(odd-even) %11 == 0

def isMod13(x):
    if(x<=52):
        return x%13 == 0
    number = str(abs(x))
    return isMod13(int(number[-1])*4 + int(number[:-1]))

def isMod17(x):
    if(x<=51):
        return x%17 == 0
    number = str(abs(x))
    return isMod17(int(number[:-1]) - 5*int(number[-1]))

def isMod19(x):
    if(x==19): return True
    elif(x<19 and x>-19): return False
    number = str(abs(x))
    return isMod19(int(number[:-1])+2*int(number[-1]))

def getListRepresentedBy(listString):
    return json.loads(listString)

def getPos(grid,searched):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if(grid[i][j]==searched):
                return j,i
    return -1,-1

def printColoredMap(listOfList):
    print("====================================")
    for l in listOfList:
        line = "".join(l)
        line = line.replace("."," ")
        line = line.replace("@",OKGREEN+"@"+ENDC)
        line = line.replace("^",OKGREEN+"^"+ENDC)
        line = line.replace("v",OKGREEN+"v"+ENDC)
        line = line.replace(">",OKGREEN+">"+ENDC)
        line = line.replace("<",OKGREEN+"<"+ENDC)
        line = line.replace("[]",WARNING+"[]"+ENDC)
        line = line.replace("#",WARNING+"#"+ENDC)
        line = line.replace("X",OKBLUE+"X"+ENDC)
        print(line)
    print("====================================")
        
def getCenteredMap(grid,x,y,size):
    return [[grid[j][i] for i in range(max(x-size,0),min(x+size,len(grid)))] for j in range(max(y-size,0),min(y+size,len(grid[0])))]

def copy(grid):
    return [[grid[j][i] for i in range(len(grid))] for j in range(len(grid[0]))]
            