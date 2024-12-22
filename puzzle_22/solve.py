import utils.utils as utils
import functools

fileName = "puzzle_22/input.txt"


def solve():
    print("Solving puzzle 22 of Advent of Code 2024")
    secrets = utils.readFileLines(fileName)
    secrets = list(map(int, secrets))
    # Part 1
    print(getSumOfFinalSecrets(secrets))
    # Part 2
    print(getMaxBananas(secrets))


def getSumOfFinalSecrets(secrets):
    '''Calculate part 1'''
    for i in range(2000):
        secrets = [getNextSecret(secret) for secret in secrets]
    return sum(secrets)


def getMaxBananas(secrets):
    '''Get all price changes and all bananas sales, then check for each possible sequence the number of bananas, and return the maximum.
    Uses a set for the sequence for each list to avoid going through them multiple times'''
    priceChangesAll = [getPriceChanges(secret) for secret in secrets]
    numBananas = [getNumBananas(secret) for secret in secrets]
    bananasPerSequence = [getBananasPerSequence(
        priceChangesAll[i], numBananas[i]) for i in range(len(priceChangesAll))]
    maxBananas = 0
    for sequence in getPossibleSequences():
        bananas = 0
        for i in range(len(bananasPerSequence)):
            if sequence in bananasPerSequence[i]:
                bananas += bananasPerSequence[i][sequence]
        if bananas > maxBananas:
            maxBananas = bananas
    return maxBananas


def getPriceChanges(initialSecret):
    '''Returns a list of priceChanges for each of the 2000 secret generated'''
    secret = initialSecret
    result = []
    for i in range(2000):
        nextSecret = getNextSecret(secret)
        result.append(nextSecret % 10 - secret % 10)
        secret = nextSecret
    return result


def getNumBananas(initialSecret):
    '''Returns a list of bananas for each of the 2000 secret generated'''
    secret = initialSecret
    result = [secret % 10]
    for i in range(2000):
        nextSecret = getNextSecret(secret)
        result.append(nextSecret % 10)
        secret = nextSecret
    return result


def getBananasPerSequence(priceChanges, bananas):
    '''Returns a list of bananas for each of the 2000 secret generated'''
    bananasPerSequence = {}
    for i in range(len(priceChanges)-4):
        sequence = tuple(priceChanges[i:i+4])
        if sequence not in bananasPerSequence:
            bananasPerSequence[sequence] = bananas[i+4]
    return bananasPerSequence


def getPossibleSequences():
    '''Returns all possible sequence. 
    Since bananas are between 0 and 9, the difference can only be between 9 and 9.
    But after a step, we know the previous number is at least or at most a number, so we can skip the impossible ones'''
    sequences = []
    for a in range(-9, 10):
        for b in range(max(-9-a, -9), min(10-a, 10)):
            for c in range(max(-9-b, -9), min(10-b, 10)):
                for d in range(max(-9-c, -9), min(10-c, 10)):
                    sequences.append(tuple([a, b, c, d]))
    return sequences


@functools.cache
def getNextSecret(secret):
    '''Returns next secret by applying the 3 steps instructed'''
    # step 1
    secret = prune(mix(secret*64, secret))
    # step 2
    secret = prune(mix(int(secret/32), secret))
    # step 3
    return prune(mix(secret*2048, secret))


def mix(value, secret):
    '''bitwise XOR operation on value and secret'''
    return value ^ secret


def prune(secret):
    '''modulo to prune with the number given'''
    return secret % 16777216
