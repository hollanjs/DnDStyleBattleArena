from Attacks import Attack
from Dice import TwentySidedDie, SixSidedDie

from enum import Enum
import random


FighterAwareness = Enum("FighterAwareness", ['FOCUSED', 'PRESENT', 'DISTRACTED'])

class Fighter:
    #general
    name: str
    hp: int
    attacks: list[Attack]

    #ability scores
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    #used for checks
    _distracted_chance: float
    _focused_chance: float
    _present_chance: float
    _awareness: FighterAwareness

    #other
    d20: TwentySidedDie



    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp
        self.attacks = []
        self.d20 = TwentySidedDie()
        self._awareness = FighterAwareness.PRESENT
        self._distracted_chance = random.randrange(1,4)/10
        self._focused_chance = random.randrange(1,4)/10
        self._present_chance = 1.0 - (self._distracted_chance + self._focused_chance)

    @staticmethod
    def score_to_modifier(score: int) -> int:
        """
        Returns the modifier for a given ability score.
        Uses the standard 5e formula: (score - 10) // 2
        """
        return (score - 10) // 2
    
    @staticmethod
    def roll_init_stat() -> int:
        rolls = [r.roll() for r in [SixSidedDie() for _ in range(4)]]

    def update_awareness(self) -> None:
        weights = [self._focused_chance, self._present_chance, self._distracted_chance]

        current_awareness = self._awareness
        new_awareness = random.choices(list(FighterAwareness), weights=weights, k=1)[0]

        if new_awareness != current_awareness:
            self.set_awareness(new_awareness)
            print(f"{self.name} became {self._awareness.name.lower()}...")

    def set_awareness(self, awareness: FighterAwareness) -> None:
        self._awareness = awareness

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
    awareness: {self._awareness.name}
    Attacks:
'''
        for atk in self.attacks:
            _string += f"\t\t{atk}\n"

        return _string