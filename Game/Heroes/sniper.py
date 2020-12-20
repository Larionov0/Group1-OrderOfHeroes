from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = "Смертельный выстрел"
    description = "Снайпер выбирает противника, и с шансом 10% убивает его.\n" \
                  "В остальных случаях он наносит 3-5 урона и оставляет ему кровотечение на 1-3 хода."
    cooldown = 4

    def cast(self, hero, my_team, enemies_team):
        sniper_vrag = hero.choose_hero_from_list(enemies_team)
        if sniper_vrag is False:
            return
        if random.randint(1, 100) <= 10:
            sniper_vrag.die()
        else:
            damage = random.randint(3, 5)
            sniper_vrag.get_damage(damage)
            duration = random.randint(1, 3)
            sniper_vrag.effects.append(effects.Bleeding(sniper_vrag, duration))
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = "мегапуля в общем"
    description = "Снайпер выбирает противника, и с шансом 50% пуля оказывается с ядом,\n" \
                  "и противник отравляется на 1-2 хода с 1-3 урона;в остальных случаях \n" \
                  "пуля оказывается с клеем, и заклеевает пасть противнику на 1-3 хода."
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        sniper_vrag = hero.choose_hero_from_list(enemies_team)
        if sniper_vrag is False:
            return
        if random.randint(1, 100) <= 50:
            damage = random.randint(1, 3)
            duration = random.randint(1, 2)
            sniper_vrag.effects.append(effects.Poisoning(sniper_vrag, duration, damage))
        else:
            duration = random.randint(1, 2)
            sniper_vrag.effects.append(effects.Silence(sniper_vrag, duration))
        sniper_vrag.get_damage(hero.attack)
        self.classic_after_cast(hero)


class Sniper(Hero):
    hp = max_hp = 19
    attack = 4
    armor = 0
    name = 'Sniper'

    skill1 = Skill1()
    skill2 = Skill2()
