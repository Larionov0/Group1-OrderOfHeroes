import random
from . import colors
from . import effects
from .skills import Skill
from os import system

from .Heroes.archer import Archer
from .Heroes.assasin import Assassin
from .Heroes.kopyrsanka import Copyrsanka
from .Heroes.ogr import Ogr
from .Heroes.blue_mage import BlueMage
from .Heroes.nekromant import Nekromant
from .Heroes.mummy import Mummy
from .Heroes.sniper import Sniper


all_heroes = [
    Archer,
    Assassin,
    Copyrsanka,
    Ogr,
    BlueMage,
    Nekromant,
    Mummy,
    Sniper
]


def clear():
    system('cls')


clear()


def input_int(text):
    while True:
        answer = input(text)
        if answer.isdigit():
            return int(answer)
        else:
            print('У вас проблемы')


def main_menu():
    while True:
        clear()
        print("--= Главное меню =--")
        print("1 - Новая игра")
        print("2 - Продолжить")
        print("3 - Стастика")
        print("4 - Магазин")
        print("5 - Выход из програмы")

        choice = input("Ваш выбор: ")
        if choice == '1':
            new_game_menu()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            break


def new_game_menu():
    while True:
        print("--= Новая игра =--")
        print('1 - игра против друга')
        print('2 - игра онлайн (в разработке)')
        print('3 - игра против ботов')
        print("4 - назад в главное меню")

        choice = input('Ваш выбор: ')
        if choice == '1':
            game_with_friend_menu()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            break


def game_with_friend_menu():
    while True:
        print('-= Игра с другом =-')
        pers_count = input_int('Сколько персонажей вы хотите: ')

        dead_list = []
        team1 = []
        team2 = []

        a = 0
        while a < pers_count:
            # выбор 1 игрока
            hero_class = choose_1_hero(1)
            team1.append(hero_class(1, team1, dead_list))

            # выбор 2 игрока
            hero_class = choose_1_hero(2)
            team2.append(hero_class(2, team2, dead_list))

            a += 1

        fight_pvp(team1, team2)
        return


def fight_pvp(team1, team2):
    round = 1
    while True:
        print(f"--= Новый раунд: {round} =--")
        for hero in team1:
            hero.hero_makes_move_menu(team1, team2)
        for hero in team2:
            hero.hero_makes_move_menu(team2, team1)

        if len(team1) == 0:
            win(2)
            return
        if len(team2) == 0:
            win(1)
            return

        round += 1


def win(player):
    print('\n\n\n\n\n\n\n\n\n\n\n\n')
    print(f"Игрок {player} победил!!!")
    input()


def choose_1_hero(player):
    while True:
        print(f"Игрок {player}, выберите героя")
        i = 1
        for hero_class in all_heroes:
            print(f"{i} - {hero_class.name}")
            i += 1

        number = input_int('Ваш выбор: ')
        hero_class = all_heroes[number - 1]
        return hero_class


def main():
    main_menu()


main()
