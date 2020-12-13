from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = "Магическое восстановление"
    description = "Некромант восстанавливает себе HP на величину, равную его магии (magic). После этого он увеличивает свой показатель магии на 1."
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        print(f"{colors.CGREEN}{hero.name} восстанавливается {colors.CEND}")
        hero.regen_hp(hero.magic)
        hero.add_magic(1)
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = "Призыв скелетона"
    description = "Некромант призывает Скелетона"
    cooldown = 5

    def cast(self, hero, my_team, enemies_team):
        skel = Skeleton(hero.team, hero.team_list, hero.dead_list)
        my_team.append(skel)
        self.classic_after_cast(hero)


class Nekromant(Hero):
    hp = max_hp = 17
    attack = 2
    armor = 0
    magic = 1
    name = 'Nekromant'

    skill1 = Skill1()
    skill2 = Skill2()

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 100) <= 30:
            self.magic += 1

    def add_magic(self, magic):
        self.magic += magic
        print(f"У {self.name} magic += {magic}. Теперь у него {self.magic}")


class Skeleton(Hero):
    name = 'Skeleton'
    hp = max_hp = 5
    attack = 2
    armor = 0

    skill1 = Skill()
    skill2 = Skill()

