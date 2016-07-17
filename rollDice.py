from random import *

def rollDice():
    x = randint(1, 6)
    y = randint(1, 6)
    z = x + y
    if x == y:
        print("CRITICAL HIT! Player rolls {} and {} for a total of {}.".format(x, y, z))
    else:
        print("Player rolls {} and {} for a total of {}.".format(x, y, z))

elcio = rollDice()
