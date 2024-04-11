import random

# bot

def bot_random_move():
    next_move = random.randint(1, 6)
    return next_move

print(bot_random_move())