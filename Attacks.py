from abc import ABC
from Dice import Die, SixSidedDie, TenSidedDie, TwelveSidedDie


class Attack(ABC):
    name: str
    dice: list[Die]

    def dice_with_extra_die(self) -> list[Die]:
        die_type = type(self.dice[0])
        return self.dice + [die_type()]

    def check_advantage(self, rolls: list[int]) -> list[int]:
        self.print_roll_results("Roll with advantage", rolls)
        min_value = min(rolls)
        print(f"removing: {min_value}")
        rolls.remove(min_value)
        return rolls

    def check_disadvantage(self, rolls: list[int]) -> list[int]:
        self.print_roll_results("Roll with disadvantage", rolls)
        max_value = max(rolls)
        print(f"removing: {max_value}")
        rolls.remove(max_value)
        return rolls

    def print_roll_results(self, message: str, results: list[int]) -> None:
        print(f"{message}:")
        print(",".join(str(num) for num in results))

    def roll_damage(self) -> int:
        results = [d.roll() for d in self.dice]
        self.print_roll_results("Role results", results)
        return sum(results)

    def roll_damage_with_advantage(self) -> int:
        results = self.check_advantage([d.roll() for d in self.dice_with_extra_die()])
        self.print_roll_results("Role results after advantage", results)
        return sum(results)

    def roll_damage_with_disadvantage(self) -> int:
        results = self.check_disadvantage([d.roll() for d in self.dice_with_extra_die()])
        self.print_roll_results("Role results after disadvantage", results)
        return sum(results)

    def __str__(self):
        return f'Attack({self.name}, damage: {len(self.dice)}{self.dice[0].name})'

class Fireball(Attack):
    def __init__(self):
        self.name = "Fireball"
        self.dice = [SixSidedDie() for _ in range(8)]

class AcidSplash(Attack):
    def __init__(self):
        self.name = "Acid Splash"
        self.dice = [SixSidedDie() for _ in range(4)]

class EldritchBlast(Attack):
    def __init__(self):
        self.name = "Eldritch Blast"
        self.dice = [TenSidedDie() for _ in range(1)]

class PoisonSpray(Attack):
    def __init__(self):
        self.name = "PoisonSpray"
        self.dice = [TwelveSidedDie() for _ in range(4)]

class Thunderclap(Attack):
    def __init__(self):
        self.name = "Thunderclap"
        self.dice = [SixSidedDie() for _ in range(4)]

class ThornWhip(Attack):
    def __init__(self):
        self.name = "Thorn Whip"
        self.dice = [SixSidedDie() for _ in range(4)]