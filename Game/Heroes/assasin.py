from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = "Критический выпад"
    description = "Ассасин выбирает одного врага. Этот враг мгновенно получает урон, равный двум атакам Ассасина. " \
                  "Если это добило врага, Ассасин восстанавливает 5 здоровья."
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        assassin_choice = hero.choose_hero_from_list(enemies_team)
        if assassin_choice is False:
            return

        assassin_choice.get_damage(hero.attack * 20)
        if assassin_choice.alive is False:
            hero.regen_hp(5)
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = "Подброс клинка"
    description = ""
    cooldown = 6

    def cast(self, hero, my_team, enemies_team):
        enemy = hero.choose_hero_from_list(enemies_team)
        delayed = effects.DelayedDamage(enemy, 2, 10, [
            effects.Bleeding(enemy, 2)
        ])
        enemy.effects.append(delayed)
        self.classic_after_cast(hero)


class Assassin(Hero):
    hp = max_hp = 16
    attack = 5
    armor = 0
    name = 'Assasin'

    skill1 = Skill1()
    skill2 = Skill2()

    def normal_attack(self, other_hero):
        print(f"{self.name} копнул {other_hero.name}")

        if random.randint(1, 100) <= 30:
            print("critical")
            other_hero.get_damage(round(self.attack * 1.5))
        else:
            other_hero.get_damage(self.attack)
        # self.did_action = True
