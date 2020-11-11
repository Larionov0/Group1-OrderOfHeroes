class Effect:
    name = 'Effect'

    def __init__(self, hero, duration):
        self.hero = hero
        self.duration = duration

    def before_move_tick(self):
        pass

    def after_move_tick(self):
        pass

    def on_ending_tick(self):
        pass


class Poisoning(Effect):
    name = 'Отравление'

    def __init__(self, hero, duration, damage):
        super().__init__(hero, duration)
        self.damage = damage

    def before_move_tick(self):
        print("Отравление в деле")
        self.hero.loose_hp(self.damage)
        self.duration -= 1
