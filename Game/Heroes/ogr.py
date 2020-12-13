from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill1(Skill):
    name = "съесть ягоду"
    description = "вы едите ягоду и пополняете половину от недостающего здоровья"
    cooldown = 4

    def cast(self, hero, my_team, enemies_team):
        a = round((hero.max_hp - hero.hp) / 2)
        hero.regen_hp(a)
        print(f'Вы съели ягоду и пополнили {a} здоровья. Теперь у вас {hero.hp} ед. здоровья.')
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = "Мышцы в жир"
    description = "Огр может потратить 10 здоровья и получить +1 броню. Это умение не отбирает его действие"
    cooldown = 3

    def cast(self, hero, my_team, enemies_team):
        print(f'Вы потратили 10 hp и получили 1 броню')
        hero.loose_hp(10)
        hero.armor += 1
        self.start_otschet()


class Ogr(Hero):
    hp = max_hp = 25
    attack = 2
    armor = 1
    name = 'Ogr'

    skill1 = Skill1()
    skill2 = Skill2()

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 2) == 1:
            self.regen_hp(1)
