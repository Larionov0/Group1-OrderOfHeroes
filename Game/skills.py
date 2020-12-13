class Skill:
    name = 'Skill'
    description = '...'
    cooldown = 2
    mana = 3

    def __init__(self):
        self.otschet = 0
        self.can_be_casted = True

    def podgotovka(self, hero, my_team, enemies_team):
        print(f"--| {self} |--")
        print(self.description)
        ans = input("Используем умение? (y/n): ")
        if ans == 'y':
            if hero.did_action is True:
                print('Вы уже совершали действие')
                return

            if not self.can_be_casted:
                print(f"Сие умение находится на перезарядке! (Осталось {self.otschet}/{self.cooldown} ходов)")
                return

            self.cast(hero, my_team, enemies_team)

    def start_otschet(self):
        self.can_be_casted = False
        self.otschet = self.cooldown

    def after_move_tick(self):
        if self.can_be_casted is False:
            self.otschet -= 1
            if self.otschet == 0:
                self.can_be_casted = True
                print(f"{self.name} восстановлен")

    def classic_after_cast(self, hero):
        hero.did_action = True
        self.start_otschet()

    def cast(self, hero, my_team, enemies_team):
        pass

    def __str__(self):
        if self.can_be_casted:
            return f"{self.name} ✔ ({self.cooldown})"
        else:
            return f"{self.name} ❌ ({self.otschet}/{self.cooldown})"
