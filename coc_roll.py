import random
import logging

logger = logging.getLogger('coc_roll')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug('coc_roll logger created')

class Die():
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        roll_res = random.randint(1, self.sides)
        logger.debug(f"Rolled a {roll_res}")
        return roll_res

class SinglesDie(Die):
    def __init__(self):
        super().__init__(10)

    def roll(self):
        roll_res = super().roll() - 1
        logger.debug(f"SinglesDie got a {roll_res}")
        return roll_res

class TensDie(Die):
    def __init__(self):
        super().__init__(10)

    def roll(self):
        roll_res = (super().roll() - 1) * 10
        logger.debug(f"TensDie got a {roll_res}")
        return roll_res

class Skill():
    def __init__(self, level):
        self.level = level


    def simple_check(self):
        die = Die(100)
        skill_check_value = die.roll()
        logger.debug(f"Skill check: {skill_check_value} <= {self.level}")
        skill_check_res = skill_check_value <= self.level
        logger.debug(f"Skill check: {skill_check_res}")
        return skill_check_res

    def check(self, num_bonus_dice=0, num_penalty_dice=0):
        logger.debug(msg=f"Skill check with num_bonus_dice: {num_bonus_dice}, num_penalty_dice: {num_penalty_dice}")
        if not num_bonus_dice and not num_penalty_dice:
            logger.debug(msg="No bonus or penalty dice, rolling simple skill check")
            return self.simple_check()

        if num_bonus_dice > 0:
            tens = [TensDie() for _ in range(num_bonus_dice + 1)]
            tens_res = min([die.roll() for die in tens])
        elif num_penalty_dice > 0:
            tens = [TensDie() for _ in range(num_penalty_dice + 1)]
            tens_res = max([die.roll() for die in tens])
        else:
            raise ValueError("num_bonus_dice and num_penalty_dice cannot both be 0")
        logger.debug(msg=f"tens_res: {tens_res}")

        singles = SinglesDie()
        skill_check_value = tens_res + singles.roll()
        logger.debug(f"Skill check: {skill_check_value} <= {self.level}")
        skill_check_res = skill_check_value <= self.level
        logger.debug(f"Skill check: {skill_check_res}")
        return skill_check_res

def simulate_skill_check(skill, num_bonus_dice=0, num_penalty_dice=0, num_simulations=1):
    successes = 0
    for _ in range(num_simulations):
        if skill.check(num_bonus_dice=num_bonus_dice, num_penalty_dice=num_penalty_dice):
            successes += 1
    print(f"Success rate: {successes / num_simulations}")


def main():
    handgun_skill = Skill(25)
    logger.setLevel(logging.WARNING)
    simulate_skill_check(handgun_skill, num_penalty_dice=1, num_simulations=400000)

if __name__ == "__main__":
    main()