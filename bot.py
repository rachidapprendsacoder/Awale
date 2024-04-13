import random
import time

# bot
weak_case = None
_case = None

def bot_random_move(situation):
    print(situation)
    time.sleep(1)
    next_move = random.randint(1, 6)
    print(next_move)
    return next_move
