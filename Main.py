from Attacks import AcidSplash, EldritchBlast, Fireball, PoisonSpray, ThornWhip, Thunderclap
from Arena import BattleMediator
from Fighters import Fighter


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