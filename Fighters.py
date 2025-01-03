from Attacks import Attack
from Dice import TwentySidedDie

from enum import Enum
import random


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