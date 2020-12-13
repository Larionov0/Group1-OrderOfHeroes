from .. import effects
from .. import colors
from ..skills import Skill
from .hero import Hero
import random


class Skill2_2(Skill):
    name = "Лечить союзника на 2хп"
    description = ""
    cooldown = 2

    def cast(self, hero, my_team, enemies_team):
        i = 0
        for hero_ in my_team:
            print(f'{i} - {hero_.short_str()}')
            i += 1
        kopyrs_choice_number = int(input())
        kopyrs_choice = my_team[kopyrs_choice_number]
        kopyrs_choice.regen_hp(2)
        self.classic_after_cast(hero)


class Kopyrsenysh(Hero):
    name = 'Kopyrsenysh'
    hp = max_hp = 6
    attack = 2
    armor = 1

    skill1 = Skill()
    skill2 = Skill2_2()


class Skill1(Skill):
    name = "Активация Высосанкомета"
    description = "Копырсанка выбирает 1 врага, затем выбирает 1 союзника (в том числе и себя). \
    Затем Высосанкомет высмактывает 3-5 здоровья из выбранного врага и восстанавливает столько же выбранному союзнику"
    cooldown = 5

    def cast(self, hero, my_team, enemies_team):
        kopyrsanka_vrag = hero.choose_hero_from_list(enemies_team)
        hp = random.randint(3, 5)
        kopyrsanka_vrag.loose_hp(hp)

        kopyrsanka_teammate = hero.choose_hero_from_list(my_team)
        kopyrsanka_teammate.regen_hp(hp)
        self.classic_after_cast(hero)


class Skill2(Skill):
    name = "Призыв копырсеныша"
    description = ""
    cooldown = 4

    def cast(self, hero, my_team, enemies_team):
        kopyrs = Kopyrsenysh(hero.team, hero.team_list, hero.dead_list)
        my_team.append(kopyrs)
        self.classic_after_cast(hero)


class Copyrsanka(Hero):
    hp = max_hp = 22
    attack = 3
    armor = 0
    name = 'Copyrsanka'

    skill1 = Skill1()
    skill2 = Skill2()

    def get_damage(self, damage):
        if random.randint(1, 100) <= 30:
            print(f'{self.name} увернулась')
            return
        remaining_damage = damage - self.armor
        print(f'{self.name} заблокировал {self.armor} урона. Получил {remaining_damage}/{damage}')
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

