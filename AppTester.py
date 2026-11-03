import random

#american wheel; 1 is red otherwise 0
def spin():
    return 1 if random.randint(1, 38) <= 18 else 0

def checkEight(spins, length = 8, contains = 6):
    
    for i in range(len(spins) - length + 1):
        countRed = 0
        for j in range(i, i + length):
            if spins[j] == 1:
                countRed += 1
        if countRed >= contains:
            return True
    return False

def AppTester():
    spins = [spin() for _ in range(100)]
    return checkEight(spins)

print(checkEight([1, 0] * 50))                                     # False
print(checkEight([0] * 50 + [1, 1, 0, 1, 1, 0, 1, 1] + [0] * 42))  # True
print(checkEight([0] * 94 + [1] * 6))                              # True

trials = 10000
print(sum(AppTester() for _ in range(trials)) / trials)

P10 = [AppTester() for _ in range(10)]
print(P10)

"""
No, I wouldn’t suspect the game is unfair. 
My simulation shows that a fair wheel produces this pattern about 97% of the time in 100 spins.
 What the user saw is normal for a fair game, not evidence of cheating.
"""