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

system('cls')


def main():
    team1 = [Archer(1), Ogr(1)]
    team2 = [Copyrsanka(2), Assassin(2), BlueMage(2)]

    round = 1
    while True:
        print(f"--= Новый раунд: {round} =--")
        for hero in team1:
            hero.hero_makes_move_menu(team1, team2)
        for hero in team2:
            hero.hero_makes_move_menu(team2, team1)

        round += 1


main()
