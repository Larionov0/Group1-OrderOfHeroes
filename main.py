import random
import colors
import effects


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
                return
            elif choice == 'i':
                self.print_heroes_info(my_team, enemies_team)
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
        print('0 - вернуться назад')
        i = 1
        for hero in enemies_team:
            print(f"{i} - {hero.short_str()}")
            i += 1

        choice = int(input('Ваш выбор: '))
        if choice == 0:
            return

        target_hero = enemies_team[choice - 1]  # выбрали цель
        self.normal_attack(target_hero)

    def before_move(self):
        self.did_action = False
        self.mana += 1
        for effect in self.effects:
            effect.before_move_tick()

    def short_str(self):
        return f"{self.get_colored_name()} ({self.hp}/{self.max_hp})"

    def __str__(self):
        return f"{self.get_colored_name()} ({self.hp}/{self.max_hp})\n" \
               f"attack={self.attack} | armor={self.armor} | mana={self.mana}/{self.max_mana} | magic={self.magic}"


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
    skill_2_name = ""

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
        i = 0
        for hero in enemies_team:
            print(f'{i} - {hero.short_str()}')
            i += 1
        asasin_choice_number = int(input())
        asasin_choice = enemies_team[asasin_choice_number]
        asasin_choice.get_damage(self.attack * 2)
        if asasin_choice.alive is False:
            self.regen_hp(5)
        self.did_action = True


class Copyrsanka(Hero):
    hp = max_hp = 22
    attack = 3
    armor = 0
    name = 'Copyrsanka'

    skill_1_name = "Активация Высосанкомета"
    skill_2_name = "Призыв копырсеныша"

    skill_1_description = "Сусанка выбирает 1 врага, затем выбирает 1 союзника (в том числе и себя). Затем Высосанкомет высмактывает 3-5 здоровья из выбранного врага и восстанавливает столько же выбранному союзнику"
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
        i = 0
        for hero in enemies_team:
            print(f'{i} - {hero.short_str()}')
            i += 1
        kopyrsanka_vrag_number = int(input())
        kopyrsanka_vrag = enemies_team[kopyrsanka_vrag_number]
        hp = random.randint(3, 5)
        kopyrsanka_vrag.loose_hp(hp)

        i = 0
        for hero in my_team:
            print(f'{i} - {hero.short_str()}')
            i += 1

        kopyrsanka_teammate_number = int(input())
        kopyrsanka_teammate = my_team[kopyrsanka_teammate_number]
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
    skill_2_name = ""

    skill_1_description = "вы едите ягоду и пополняете половину от недостающего здоровья"
    skill_2_description = ""

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.alive and random.randint(1, 2) == 1:
            self.regen_hp(1)

    def cast_1_skill(self, my_team, enemies_team):
        a = round((self.max_hp - self.hp)/2)
        self.hp += a
        print(f'Вы съели ягоду и пополнили {a} здоровья. Теперь у вас {self.hp} ед. здоровья.')
        self.did_action = True


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


class Skeleton(Hero):
    name = 'Skeleton'
    hp = max_hp = 5
    attack = 2
    armor = 0
    skill_1_name = "Ничего не делать"
    skill_2_name = "Ничего не делать"

    skill_1_description = "Не работать"
    skill_2_description = "Не работать"


def main():
    team1 = [Archer(1), Ogr(1), Nekromant(1)]
    team2 = [Copyrsanka(2), Assassin(2)]

    round = 1
    while True:
        print(f"--= Новый раунд: {round} =--")
        for hero in team1:
            hero.hero_makes_move_menu(team1, team2)
        for hero in team2:
            hero.hero_makes_move_menu(team2, team1)

        round += 1


main()
