from .. import effects
from .. import colors
from ..skills import Skill
import random
from ..Savings.save import save_data


class Hero:
    name = 'Hero'

    hp = max_hp = 0
    mana = max_mana = 0
    attack = 0
    armor = 0
    magic = 0

    skill_1_name = "Отравление"
    skill_2_name = "Град стрел"

    skill_1_description = ""
    skill_2_description = ""

    alive = True

    did_action = False
    can_do_move = True
    can_be_damaged = True

    skill1 = Skill()
    skill2 = Skill()

    def __init__(self, team, team_list, dead_list):
        self.team = team
        self.effects = []
        self.team_list = team_list
        self.dead_list = dead_list
        self.skill1 = self.skill1
        self.skill2 = self.skill2

    def get_color(self):
        if self.team == 1:
            return colors.CBLUE
        else:
            return colors.CRED

    def get_colored_name(self):
        return f"{self.get_color()}{self.name}{colors.CEND}"

    def get_damage(self, damage):
        if self.can_be_damaged is False:
            print(f'Герой {self.get_colored_name()} не может быть продамажен')
            return

        remaining_damage = damage - self.armor
        print(f'{self.name} заблокировал {self.armor} урона. Получил {remaining_damage}/{damage}')
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

    def loose_hp(self, hp):
        self.hp -= hp
        print(f"{self.name} ранен на {hp} hp. У него осталось {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.die()

    def die(self):
        if self.alive is True:
            self.alive = False
            self.team_list.remove(self)
            self.dead_list.append(self)
            print(f"{self.name} мертв. Помним. Любим. Скорбим.")

    def regen_hp(self, hp):
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} отлечился на {hp} hp. Теперь у него {self.hp}/{self.max_hp}")

    def normal_attack(self, other_hero):
        print(f"{self.name} копнул {other_hero.name}")
        other_hero.get_damage(self.attack)
        self.did_action = True

    def cast_1_skill(self, my_team, enemies_team):
        pass

    def cast_2_skill(self, my_team, enemies_team):
        pass

    def hero_makes_move_menu(self, my_team, enemies_team, data):
        self.before_move()
        if self.can_do_move and self.alive:
            while True:
                print(f"--= Ходит {self.name} ({self.team}) =--")
                text = f"{self}\n" \
                       "a - обычная атака\n" \
                       f"1 - первое умение ({colors.CGREEN2}{self.skill1}{colors.CEND})\n" \
                       f"2 - второе умение ({colors.CGREEN2}{self.skill2}{colors.CEND})\n" \
                       "- - пропустить ход\n" \
                       "i - информация про героев\n" \
                       "s - настройки\n" \
                       "Ваш выбор: "
                choice = input(text)
                if choice == 'a':
                    self.normal_attack_menu(enemies_team)
                elif choice == '1':
                    self.skill1.podgotovka(self, my_team, enemies_team)
                elif choice == '2':
                    self.skill2.podgotovka(self, my_team, enemies_team)
                elif choice == '-':
                    break
                elif choice == 'i':
                    self.print_heroes_info(my_team, enemies_team)
                elif choice == 's':
                    self.settings(data)
                else:
                    pass
        else:
            print(f"{self.get_colored_name()} лишен хода")

        self.after_move()

    def settings(self, data):
        while True:
            print('---= Настройки =---')
            print('1 - сохранить')
            print('2 - выйти')

            choice = input("Ваш выбор: ")
            if choice == '1':
                save_data(data)
                input('Данные успешно сохранены')
            elif choice == '2':
                pass
            else:
                pass

    def print_heroes_info(self, my_team, enemies_team):
        for hero in my_team + enemies_team:
            print('-' * 40)
            print(hero)
            print('-' * 40)

    def normal_attack_menu(self, enemies_team):
        if self.did_action is True:
            print(f"{self.name} уже совершал атаку:(")
            return

        target_hero = self.choose_hero_from_list(enemies_team)
        if target_hero:
            self.normal_attack(target_hero)
        else:
            return

    def before_move(self):
        self.can_do_move = True
        self.did_action = False
        self.can_be_damaged = True
        self.mana += 1
        for effect in self.effects:
            effect.before_move_tick()

    def after_move(self):
        for effect in self.effects:
            effect.after_move_tick()
        for skill in [self.skill1, self.skill2]:
            skill.after_move_tick()

    def choose_hero_from_list(self, heroes, text='--= Выберите героя =--'):
        print(text)
        print('0 - вернуться назад')
        i = 1
        for hero in heroes:
            print(f"{i} - {hero.short_str()}")
            i += 1

        choice = int(input('Ваш выбор: '))
        if choice == 0:
            return False

        if choice < 0 or choice > len(heroes):
            print("Такого варианта у вас нет")
            return False

        return heroes[choice - 1]  # выбрали цель и вернули ее

    def short_str(self):
        return f"{self.get_colored_name()} ({self.hp}/{self.max_hp})"

    def __str__(self):
        effects_text = ''
        for effect in self.effects:
            effects_text += f'- {effect}\n'
        return f"{self.get_colored_name()} ({self.hp}/{self.max_hp})\n" \
               f"{self.skill1}  |  {self.skill2}\n" \
               f"attack={self.attack} | armor={self.armor} | mana={self.mana}/{self.max_mana} | magic={self.magic}\n" \
               f"{effects_text}"
