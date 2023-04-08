import random
import logging
import statistics

logger = logging.getLogger('coc_roll')
# logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

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


def get_weapon_damage(max_damage=8):
    die = Die(max_damage)
    return die.roll()


def simulate_multiple_shots(skill_level=25, num_shots=1, gun_max_damage=8, num_simulations=10):

    skill = Skill(skill_level)

    successes = 0
    num_penalty_dice = 0

    if num_shots > 1:
        num_penalty_dice = 1

    damage_distribution = {}
    for _ in range(num_simulations):
        total_damage = 0
        for _ in range(num_shots):
            if skill.check(num_penalty_dice=num_penalty_dice):
                # calculate damage
                damage = get_weapon_damage(max_damage=gun_max_damage)
                total_damage += damage
        logger.debug(f"total_damage: {total_damage}")
        damage_distribution[total_damage] = damage_distribution.get(total_damage, 0) + 1

    logger.debug(f"damage_distribution: {damage_distribution}")
    return damage_distribution


def simulate_rate_of_success(skill_level=25, num_shots=1, num_penalty_dice=0, num_simulations=10):
    skill = Skill(skill_level)

    successes = 0

    for _ in range(num_simulations):
        if skill.check(num_penalty_dice=num_penalty_dice):
            successes += 1

    success_rate = successes / num_simulations
    print(f"Success rate: {success_rate}")
    return success_rate


def main():
    handgun_skill = Skill(25)
    handgun_damage = 8
    # logger.setLevel(logging.DEBUG)
    # res = simulate_multiple_shots(
    #     skill_level=25, 
    #     num_shots=3,
    #     gun_max_damage=handgun_damage,
    #     num_simulations=100
    # )

    res = simulate_rate_of_success(
        skill_level=25, 
        num_shots=3,
        num_penalty_dice=1,
        num_simulations=10000
    )
    print(res)

if __name__ == "__main__":
    main()