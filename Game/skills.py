class Skill:
    name = 'Skill'
    description = '...'
    cooldown = 2
    mana = 3

    def podgotovka(self, hero, my_team, enemies_team):
        print(f"--| {self.name} |--")
        print(self.description)
        ans = input("Используем умение? (y/n): ")
        if ans == 'y':
            if hero.did_action is True:
                print('Вы уже совершали действие')
            else:
                self.cast(hero, my_team, enemies_team)

    def cast(self, hero, my_team, enemies_team):
        pass
