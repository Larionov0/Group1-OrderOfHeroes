from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = 'Замотка'
    description = 'Мумия обматывает бинтами выбранного противника, оглушая его на ход и нанося 3-6 урона\n' \
                  'и оставляет кровотечение на ход'
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        enemy = hero.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        enemy.get_damage(random.randint(3, 6))
        stun = effects.Stun(enemy, 1)
        bleeding = effects.Bleeding(enemy, 1)
        enemy.effects.append(stun)
        enemy.effects.append(bleeding)
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = 'Защитный кокон'
    description = 'Мумия обволакивает выбранного союзника с < чем половиной здоровья защитным коконом\n' \
                  'на ход. Он блокирует любой физический урон'
    cooldown = 4

    def cast(self, hero, my_team, enemies_team):
        suitable_heroes = []
        for hero_ in my_team:
            if hero_.hp <= round(hero_.max_hp / 2):
                suitable_heroes.append(hero_)
        teammate_hero = hero.choose_hero_from_list(suitable_heroes)
        if teammate_hero is None:
            return

        teammate_hero.effects.append(effects.FlawlessProtection(teammate_hero, 1))
        self.classic_after_cast(hero)


class Mummy(Hero):
    name = 'Mummy'
    hp = max_hp = 25
    attack = 2
    armor = 1

    skill1 = Skill1()
    skill2 = Skill2()
