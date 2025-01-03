from abc import ABC, abstractmethod
from enum import Enum
import random
import uuid

random.seed(int(uuid.uuid4()))

class Die(ABC):
    name: str

    @abstractmethod
    def roll(self) -> int:
        pass

class SixSidedDie(Die):
    def __init__(self):
        self.name = "d6"

    def roll(self) -> int:
        return random.randint(1,6)

class TenSidedDie(Die):
    def __init__(self):
        self.name = "d10"

    def roll(self) -> int:
        return random.randint(1,10)

class TwelveSidedDie(Die):
    def __init__(self):
        self.name = "d12"

    def roll(self) -> int:
        return random.randint(1,12)

class TwentySidedDie(Die):
    def __init__(self):
        self.name = "d20"

    def roll(self) -> int:
        return random.randint(1,20)

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

FighterAwareness = Enum("FighterAwareness", ['FOCUSED', 'PRESENT', 'DISTRACTED'])

class Fighter:
    _distracted_chance: float
    _focused_chance: float

    _present_chance: float

    name: str
    hp: int
    d20: TwentySidedDie
    awareness: FighterAwareness
    attacks: list[Attack]

    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        self.attacks = []
        self.d20 = TwentySidedDie()
        self.awareness = FighterAwareness.PRESENT
        self._distracted_chance = random.randrange(1,4)/10
        self._focused_chance = random.randrange(1,4)/10
        self._present_chance = 1.0 - (self._distracted_chance + self._focused_chance)

    def update_awareness(self) -> None:
        weights = [self._focused_chance, self._present_chance, self._distracted_chance]

        current_awareness = self.awareness
        new_awareness = random.choices(list(FighterAwareness), weights=weights, k=1)[0]

        if new_awareness != current_awareness:
            self.set_awareness(new_awareness)
            print(f"{self.name} became {self.awareness.name.lower()}...")

    def set_awareness(self, awareness: FighterAwareness) -> None:
        self.awareness = awareness

    def learn_attack(self, attack: Attack) -> None:
        if attack not in self.attacks:
            self.attacks.append(attack)

    def attack(self, attack: Attack) -> int:
        if attack in self.attacks:
            print(f"Casting {attack.name}")
            return attack.roll_damage()

    def attack_with_advantage(self, attack: Attack) -> int:
        if attack in self.attacks:
            print(f"Casting {attack.name} with advantage")
            return attack.roll_damage_with_advantage()

    def attack_with_disadvantage(self, attack: Attack) -> int:
        if attack in self.attacks:
            print(f"Casting {attack.name} with disadvantage")
            return attack.roll_damage_with_disadvantage()

    def roll_d20(self):
        return self.d20.roll()

    def __str__(self):
        _string = f'''Fighter: {self.name}
    {self.hp} hp
    awareness: {self.awareness.name}
    Attacks:
'''
        for atk in self.attacks:
            _string += f"\t\t{atk}\n"

        return _string

class BattleMediator:
    _battle_in_progress = False
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BattleMediator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def print_fighter_status(fighters: tuple[Fighter, ...]) -> None:
        print("  ---v---   ".join([f"{f.name} ({f.awareness.name}): {f.hp} HP" for f in fighters]))
        print()

    @staticmethod
    def announce_fighters(*fighters) -> None:
        print("Fighters in current battle:")
        for fighter in fighters:
            print(fighter)

    @staticmethod
    def roll_initiative(fighter1: Fighter, fighter2: Fighter) -> tuple[Fighter, Fighter]:
        if fighter1.roll_d20() > fighter2.roll_d20():
            return (fighter1, fighter2)
        else:
            return (fighter2, fighter1)

    @staticmethod
    def start_battle(fighter1: Fighter, fighter2: Fighter) -> None:
        BattleMediator._battle_in_progress = True
        BattleMediator.battle(fighter1, fighter2)

    @staticmethod
    def end_battle() -> None:
        BattleMediator._battle_in_progress = False

    @staticmethod
    def attack(attacker: Fighter, defender: Fighter, attack: Attack):
        attack_roll = attacker.roll_d20()
        defense_roll = defender.roll_d20()

        if attack_roll > defense_roll:
            print(f"{attacker.name} hit {defender.name} with {attack.name} (rolling for damage)")
            match attacker.awareness:
                case FighterAwareness.FOCUSED:
                    damage = attacker.attack_with_advantage(attack)
                case FighterAwareness.DISTRACTED:
                    damage = attacker.attack_with_disadvantage(attack)
                case _:
                    damage = attacker.attack(attack)

            print(f"{attacker.name}'s {attack.name} caused {damage} damage to {defender.name}")
            defender.hp -= damage
        else:
            print(f"{attacker.name} missed {defender.name} with {attack.name}")

        if defender.hp <= 0:
            BattleMediator.end_battle()
            print(f"{defender.name} has perished in battle against {attacker.name}")

    @staticmethod
    def battle(fighter1: Fighter, fighter2: Fighter):
        BattleMediator.announce_fighters(fighter1, fighter2)
        attacker, defender = BattleMediator.roll_initiative(fighter1, fighter2)
        while BattleMediator._battle_in_progress:
            attacker.update_awareness()
            BattleMediator.attack(attacker, defender, random.choice(attacker.attacks))
            BattleMediator.print_fighter_status((attacker, defender))
            attacker, defender = defender, attacker

if __name__ == '__main__':

    # init fighters
    fighter1 = Fighter("Chrulk", 100)
    fighter2 = Fighter("Steve", 100)

    # create available attack pool
    available_attacks = [Fireball, AcidSplash, EldritchBlast, PoisonSpray, Thunderclap, ThornWhip]

    # train fighters
    for attack in available_attacks:
        fighter1.learn_attack(attack())
        fighter2.learn_attack(attack())

    Arena = BattleMediator()
    Arena.start_battle(fighter1, fighter2)
