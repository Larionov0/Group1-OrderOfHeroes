from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = 'Эффектный'
    description = "Накладываем эффекты"
    cooldown = 4

    def cast(self, hero, my_team, enemies_team):
        for hero_ in enemies_team:
            hero_.effects.append(effects.Poisoning(hero, 2, 2))
            hero_.effects.append(effects.Bleeding(hero, 2))


class Skill2(Skill):
    name = 'Град стрел'
    description = "Лучник запускае град стрел во всех врагов, и каждый\n" \
                          "получает 2-5 урона."
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        print(f"{colors.CGREEN}{hero.name} запускает град стрел{colors.CEND}")
        for hero_ in enemies_team:
            hero_.get_damage(random.randint(2, 5))
        hero.did_action = True


class Archer(Hero):
    hp = max_hp = 15
    attack = 5
    armor = 0
    name = 'Archer'

    skill1 = Skill1()
    skill2 = Skill2()

    def normal_attack(self, other_hero):
        print(f"{self.name} запустил стрелу в {other_hero.name}")

        if random.randint(1, 100) <= 30:
            print('он промахнулся:(')
        else:
            other_hero.get_damage(self.attack)
        self.did_action = True
