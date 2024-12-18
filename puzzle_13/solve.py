import utils.utils as utils

fileName = "puzzle_13/input.txt"


def solve():
    print("Solving puzzle 13 of Advent of Code 2024")
    buttonsAndPrizes = utils.readLinesSeparatedByEmptyLines(fileName)
    
    games = getGames(buttonsAndPrizes)
    
    print(sum([getTokensToWin(game) for game in games]))
    
    print(sum([getTokensToWin(fixGame(game)) for game in games]))

def getGames(buttonsAndPrizes):
    games = []
    for a,b,prize in buttonsAndPrizes:
        xa,ya=a.replace("Button A: X+","").replace("Y+","").split(", ")
        xb,yb=b.replace("Button B: X+","").replace("Y+","").split(", ")
        xprize,yprize = prize.replace("Prize: X=","").replace("Y=","").split(", ")
        games.append(list(map(int,[xa,ya,xb,yb,xprize,yprize])))
    return games

def fixGame(game):
    xa,ya,xb,yb,xprize,yprize = game
    return [xa,ya,xb,yb,xprize+10_000_000_000_000,yprize+10_000_000_000_000]

def getTokensToWin(game):
    '''Search the number of tokens needed to win, 0 if unwinnable.
    Equation to resolve:
    k*xa + l*xb = xprize
    k*ya + l*yb = yprize
    3k+l minimized
    xa,xb,ya,yb != 0
    =>
    k*xa*ya + l*xb*ya = xprize*ya
    k*ya*xa + l*yb*xa = yprize*xa
    =>
    l*xb*ya - l*yb*xa = xprize*ya - yprize*xa
    
    l = (xprize*ya - yprize*xa) / (xb*ya - yb*xa)
    => k = (xprize - l*xb)/xa
    
    if (xb*ya - yb*xa == 0) => do something? +> doesn't seem to happen here so no
    '''
    xa,ya,xb,yb,xprize,yprize = game
    
    nbB = int((xprize*ya - yprize*xa) / (xb*ya - yb*xa))
    nbA = int((xprize - nbB*xb)/xa)
    # check if results weren't with non positive integer button presses
    resultX = nbB*xb +nbA*xa
    resultY = nbB*yb + nbA*ya
    if nbA >=0 and nbB >= 0 and resultX == xprize and resultY == yprize:
        return nbA*3 + nbB
    else:
        return 0