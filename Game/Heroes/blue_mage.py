from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = 'Магический шар'
    description = "Маг запускает ультрамагический шар в выбранного врага, нанося тому 3-14 урона"
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        target_hero = hero.choose_hero_from_list(enemies_team)
        if target_hero is None:
            return

        target_hero.loose_hp(random.randint(3, 14))
        print(f"{colors.CGREEN}{hero.name} запускает магический шар{colors.CEND}")
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = 'Массовое опупение'
    description = "Каждый враг имеет 30 % шанс быть оглушенным"
    cooldown = 6

    def cast(self, hero, my_team, enemies_team):
        print(f"{colors.CGREEN}{hero.name} запускает магический шар{colors.CEND}")
        for enemy in enemies_team:
            if random.randint(1, 100) <= 40:
                enemy.effects.append(effects.Stun(enemy, 1))
                print(f"{enemy.name} в состоянии опупения")
        self.classic_after_cast(hero)


class BlueMage(Hero):
    hp = max_hp = 15
    attack = 3
    armor = 0
    name = 'BlueMage'

    skill1 = Skill1()
    skill2 = Skill2()
