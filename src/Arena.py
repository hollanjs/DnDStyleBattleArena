from Attacks import Attack
from Fighters import Fighter, FighterAwareness

import random


class BattleMediator:
    _battle_in_progress = False
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BattleMediator, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def print_fighter_status(fighters: tuple[Fighter, ...]) -> None:
        print(
            "  ---v---   ".join([f"{f.name} ({f._awareness.name}): {f.hp} HP" for f in fighters]))
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
            print(f"{attacker.name} hit {defender.name} with {
                  attack.name} (rolling for damage)")
            match attacker._awareness:
                case FighterAwareness.FOCUSED:
                    damage = attacker.attack_with_advantage(attack)
                case FighterAwareness.DISTRACTED:
                    damage = attacker.attack_with_disadvantage(attack)
                case _:
                    damage = attacker.attack(attack)

            print(f"{attacker.name}'s {attack.name} caused {
                  damage} damage to {defender.name}")
            defender.hp -= damage
        else:
            print(f"{attacker.name} missed {defender.name} with {attack.name}")

        if defender.hp <= 0:
            BattleMediator.end_battle()
            print(f"{defender.name} has perished in battle against {
                  attacker.name}")

    @staticmethod
    def battle(fighter1: Fighter, fighter2: Fighter):
        BattleMediator.announce_fighters(fighter1, fighter2)
        attacker, defender = BattleMediator.roll_initiative(fighter1, fighter2)
        while BattleMediator._battle_in_progress:
            attacker.update_awareness()
            BattleMediator.attack(attacker, defender,
                                  random.choice(attacker.attacks))
            BattleMediator.print_fighter_status((attacker, defender))
            attacker, defender = defender, attacker
