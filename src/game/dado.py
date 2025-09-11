import random

def get_dice():
    try:
        dice_0 = random.randint(1, 6)
        dice_1 = random.randint(1, 6)
        if dice_0 == dice_1:
            return  (dice_0, dice_1, dice_0, dice_1, )
        else:
            return  (dice_0, dice_1, )
    except Exception as e:
        return ()           