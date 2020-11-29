import random
from . import colors
from . import effects
from os import system

system('cls')


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

    def __init__(self, team):
        self.team = team
        self.effects = []

    def get_color(self):
        if self.team == 1:
            return colors.CBLUE
        else:
            return colors.CRED

    def get_colored_name(self):
        return f"{self.get_color()}{self.name}{colors.CEND}"

    def get_damage(self, damage):
        remaining_damage = damage - self.armor
        print(f'{self.name} заблокировал {self.armor} урона. Получил {remaining_damage}/{damage}')
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

    def loose_hp(self, hp):
        self.hp -= hp
        print(f"{self.name} ранен на {hp} hp. У него осталось {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.alive = False
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

    def hero_makes_move_menu(self, my_team, enemies_team):
        self.before_move()
        if self.can_do_move:
            while True:
                print(f"--= Ходит {self.name} ({self.team}) =--")
                text = f"{self}\n" \
                       "a - обычная атака\n" \
                       "1 - первое умение\n" \
                       "2 - второе умение\n" \
                       "- - пропустить ход\n" \
                       "i - информация про героев\n" \
                       "Ваш выбор: "
                choice = input(text)
                if choice == 'a':
                    self.normal_attack_menu(enemies_team)
                elif choice == '1':
                    print(f"--| {self.skill_1_name} |--")
                    print(self.skill_1_description)
                    ans = input("Используем умение? (y/n): ")
                    if ans == 'y':
                        if self.did_action is True:
                            print('Вы уже совершали действие')
                        else:
                            self.cast_1_skill(my_team, enemies_team)
                elif choice == '2':
                    print(f"--| {self.skill_2_name} |--")
                    print(self.skill_2_description)
                    ans = input("Используем умение? (y/n): ")
                    if ans == 'y':
                        if self.did_action is True:
                            print('Вы уже совершали действие')
                        else:
                            self.cast_2_skill(my_team, enemies_team)
                elif choice == '-':
                    break
                elif choice == 'i':
                    self.print_heroes_info(my_team, enemies_team)
                else:
                    pass
        else:
            print(f"{self.get_colored_name()} лишен хода")

        self.after_move()

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
        self.mana += 1
        for effect in self.effects:
            effect.before_move_tick()

    def after_move(self):
        for effect in self.effects:
            effect.after_move_tick()

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
               f"attack={self.attack} | armor={self.armor} | mana={self.mana}/{self.max_mana} | magic={self.magic}\n" \
               f"{effects_text}"


class Archer(Hero):
    hp = max_hp = 15
    attack = 5
    armor = 0
    name = 'Archer'

    skill_1_name = ""
    skill_2_name = "Град стрел"
    skill_1_description = ""
    skill_2_description = "Лучник запускае град стрел во всех врагов, и каждый\n" \
                          "получает 2-5 урона."

    def normal_attack(self, other_hero):
        print(f"{self.name} запустил стрелу в {other_hero.name}")

        if random.randint(1, 100) <= 30:
            print('он промахнулся:(')
        else:
            other_hero.get_damage(self.attack)
        self.did_action = True

    def cast_1_skill(self, my_team, enemies_team):
        for hero in enemies_team:
            hero.effects.append(effects.Poisoning(hero, 2, 2))
            hero.effects.append(effects.Bleeding(hero, 2))

    def cast_2_skill(self, my_team, enemies_team):
        print(f"{colors.CGREEN}{self.name} запускает град стрел{colors.CEND}")
        for hero in enemies_team:
            hero.get_damage(random.randint(2, 5))
        self.did_action = True


class Assassin(Hero):
    hp = max_hp = 16
    attack = 5
    armor = 0
    name = 'Assasin'

    skill_1_name = "Критический выпад"
    skill_2_name = "Подброс клинка"

    skill_1_description = "Ассасин выбирает одного врага. Этот враг мгновенно получает урон, равный двум атакам Ассасина. " \
                          "Если это добило врага, Ассасин восстанавливает 5 здоровья."
    skill_2_description = ""

    def normal_attack(self, other_hero):
        print(f"{self.name} копнул {other_hero.name}")

        if random.randint(1, 100) <= 30:
            print("critical")
            other_hero.get_damage(round(self.attack * 1.5))
        else:
            other_hero.get_damage(self.attack)
        # self.did_action = True

    def cast_1_skill(self, my_team, enemies_team):
        assassin_choice = self.choose_hero_from_list(enemies_team)
        if assassin_choice is False:
            return

        assassin_choice.get_damage(self.attack * 2)
        if assassin_choice.alive is False:
            self.regen_hp(5)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        delayed = effects.DelayedDamage(enemy, 2, 10, [
            effects.Bleeding(enemy, 2)
        ])
        enemy.effects.append(delayed)


class Copyrsanka(Hero):
    hp = max_hp = 22
    attack = 3
    armor = 0
    name = 'Copyrsanka'

    skill_1_name = "Активация Высосанкомета"
    skill_2_name = "Призыв копырсеныша"

    skill_1_description = "Копырсанка выбирает 1 врага, затем выбирает 1 союзника (в том числе и себя). Затем Высосанкомет высмактывает 3-5 здоровья из выбранного врага и восстанавливает столько же выбранному союзнику"
    skill_2_description = ""

    def get_damage(self, damage):
        if random.randint(1, 100) <= 30:
            print(f'{self.name} увернулась')
            return
        remaining_damage = damage - self.armor
        print(f'{self.name} заблокировал {self.armor} урона. Получил {remaining_damage}/{damage}')
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

    def cast_1_skill(self, my_team, enemies_team):
        kopyrsanka_vrag = self.choose_hero_from_list(enemies_team)
        hp = random.randint(3, 5)
        kopyrsanka_vrag.loose_hp(hp)

        kopyrsanka_teammate = self.choose_hero_from_list(my_team)
        kopyrsanka_teammate.regen_hp(hp)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        kopyrs = Kopyrsenysh(self.team)
        my_team.append(kopyrs)
        self.did_action = True


class Kopyrsenysh(Hero):
    name = 'Kopyrsenysh'
    hp = max_hp = 6
    attack = 2
    armor = 1
    skill_1_name = "Ничего не делать"
    skill_2_name = "Лечить союзника на 2хп"

    skill_1_description = ""
    skill_2_description = ""

    def cast_2_skill(self, my_team, enemies_team):
        i = 0
        for hero in my_team:
            print(f'{i} - {hero.short_str()}')
            i += 1
        kopyrs_choice_number = int(input())
        kopyrs_choice = my_team[kopyrs_choice_number]
        kopyrs_choice.regen_hp(2)
        self.did_action = True


class Ogr(Hero):
    hp = max_hp = 25
    attack = 2
    armor = 1
    name = 'Ogr'

    skill_1_name = "съесть ягоду"
    skill_2_name = "Мышцы в жир"

    skill_1_description = "вы едите ягоду и пополняете половину от недостающего здоровья"
    skill_2_description = "Огр может потратить 10 здоровья и получить +1 броню. Это умение не отбирает его действие"

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 2) == 1:
            self.regen_hp(1)

    def cast_1_skill(self, my_team, enemies_team):
        a = round((self.max_hp - self.hp) / 2)
        self.hp += a
        print(f'Вы съели ягоду и пополнили {a} здоровья. Теперь у вас {self.hp} ед. здоровья.')
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        print(f'Вы потратили 10 hp и получили 1 броню')
        self.loose_hp(10)
        self.armor += 1


class Nekromant(Hero):
    hp = max_hp = 17
    attack = 2
    armor = 0
    magic = 1
    name = 'Nekromant'

    skill_1_name = "Магическое восстановление"
    skill_2_name = "Призыв скелетона"
    skill_1_description = "Некромант восстанавливает себе HP на величину, равную его магии (magic). После этого он увеличивает свой показатель магии на 1."
    skill_2_description = "Некромант призывает Скелетона"

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 100) <= 30:
            self.magic += 1

    def cast_1_skill(self, my_team, enemies):
        print(f"{colors.CGREEN}{self.name} восстанавливается {colors.CEND}")
        self.regen_hp(self.magic)
        self.add_magic(1)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        skel = Skeleton(self.team)
        my_team.append(skel)
        self.did_action = True

    def add_magic(self, magic):
        self.magic += magic
        print(f"У {self.name} magic += {magic}. Теперь у него {self.magic}")


class Mummy(Hero):
    name = 'Mummy'
    hp = max_hp = 20
    attack = 2
    armor = 1

    skill_1_name = 'Замотка'
    skill_2_name = ''

    skill_1_description = 'Мумия обматывает бинтами выбранного противника, оглушая его на ход и нанося 3-6 урона\n' \
                          'и оставляет кровотечение на ход'
    skill_2_description = ''

    def cast_1_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        enemy.get_damage(random.randint(3, 6))
        stun = effects.Stun(enemy, 1)
        bleeding = effects.Bleeding(enemy, 1)
        enemy.effects.append(stun)
        enemy.effects.append(bleeding)


class Skeleton(Hero):
    name = 'Skeleton'
    hp = max_hp = 5
    attack = 2
    armor = 0
    skill_1_name = "Ничего не делать"
    skill_2_name = "Ничего не делать"

    skill_1_description = "Не работать"
    skill_2_description = "Не работать"


class Sniper(Hero):
    hp = max_hp = 19
    attack = 4
    armor = 0
    name = 'Sniper'

    skill_1_name = "Смертельный выстрел"
    skill_2_name = "мегапуля в общем"

    skill_1_description = "Снайпер выбирает противника, и с шансом 10% убивает его. В остальных случаях он наносит 3-5 урона и оставляет ему кровотечение на 1-3 хода."
    skill_2_description = "Снайпер выбирает противника, и с шансом 50% пуля оказывается с ядом, и противник отравляется на 1-2 хода с 1-3 урона;в остальных случаях пуля оказывается с клеем, и заклеевает пасть противнику на 1-3 хода."

    def cast_1_skill(self, my_team, enemies_team):
        sniper_vrag = self.choose_hero_from_list(enemies_team)
        if sniper_vrag is False:
            return
        if random.randint(1, 100) <= 10:
            sniper_vrag.alive = False
        else:
            damage = random.randint(3, 5)
            sniper_vrag.get_damage(damage)
            duration = random.randint(1, 3)
            sniper_vrag.effects.append(effects.Bleeding(sniper_vrag, duration))
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        sniper_vrag = self.choose_hero_from_list(enemies_team)
        if sniper_vrag is False:
            return
        if random.randint(1, 100) <= 50:
            damage = random.randint(1, 3)
            duration = random.randint(1, 2)
            sniper_vrag.effects.append(effects.Poisoning(sniper_vrag, duration, damage))
        else:
            duration = random.randint(1, 3)
            sniper_vrag.effects.append(effects.Silence(sniper_vrag, duration))
        sniper_vrag.get_damage(self.attack)
        self.did_action = True


class Naruto(Hero):
    name = 'Наруто'
    hp = max_hp = 20
    attack = 4
    armor = 0
    skill_1_name = "тенивое клонирование"
    skill_2_name = "расенган"

    skill_1_description = "призвать клона"
    skill_2_description = "сделать воздушную бомбу"

    def cast_1_skill(self, my_team, enemies_team):
        naruto = Naruto2(self.team)
        my_team.append(naruto)
        self.did_action = True
        for enemy in enemies_team:
            bleeding = effects.Bleeding(enemy, 1)
            enemy.effects.append(bleeding)
        print("от множества клонов у противника закрутилась голова и пошла кровь")

    def cast_2_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        enemy.get_damage(self.attack + self.attack)
        stun = effects.Stun(enemy, 1)
        enemy.effects.append(stun)
        print("ваш враг потерял бдительность, вы сможете его ударить еще раз")


class Naruto2(Hero):
    name = 'Наруто'
    hp = max_hp = 12
    attack = 3
    armor = 0
    skill_1_name = ""
    skill_2_name = ""

    skill_1_description = ""
    skill_2_description = ""


class Shadow_guard(Hero):
    name = "Shadow guard"
    hp = max_hp = 18
    attack = 5
    armor = 1
    skill_1_name = "тенывое дыхание"
    skill_2_name = "тенивое востановление"
    skill_1_description = "страж поджигает виброного врага "
    skill_2_description = ""

    def cast_1_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        sbreath = effects.Arson(enemy, 7)
        enemy.effects.append(sbreath)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        sregen = effects.DelayedHeeling(self, 2, 10)
        self.effects.append(sregen)
        self.did_action = True


class Geometrical_Dominator(Hero):
    hp = max_hp = 30
    attack = 3
    armor = 1
    name = 'Повелитель Вальххалы'

    skill_1_name = "Дар Гьяллархорна"
    skill_2_name = "Таранящий парализатоп"

    skill_1_description = "Поднимает здоровье любого союзника"
    skill_2_description = "Вы лишаете врага возможностей применять скилы"

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 2) == 1:
            self.regen_hp(1)

    def cast_1_skill(self, my_team, enemies_team):
        team_mate = self.choose_hero_from_list(my_team)
        if team_mate is False:
            return
        delayed = effects.DelayedRegen(team_mate, 2, 10)
        team_mate.effects.append(delayed)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        cycles = effects.Silence(enemy, 1)
        enemy.effects.append(cycles)
        self.did_action = True


def main():
    team1 = [Archer(1), Ogr(1), Nekromant(1)]
    team2 = [Copyrsanka(2), Assassin(2), Mummy(2)]

    round = 1
    while True:
        print(f"--= Новый раунд: {round} =--")
        for hero in team1:
            hero.hero_makes_move_menu(team1, team2)
        for hero in team2:
            hero.hero_makes_move_menu(team2, team1)

        round += 1


main()