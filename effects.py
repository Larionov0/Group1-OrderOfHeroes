import colors


class Effect:
    name = 'Effect'

    def __init__(self, hero, duration):
        self.hero = hero
        self.duration = duration

    def decrease_duration(self):
        self.duration -= 1
        print(
            f"{colors.CVIOLET}У {self.hero.name} еффект {self.name} подуменьшился. Осталось {self.duration} ходов{colors.CEND}")
        if self.duration == 0:
            self.die()

    def die(self):
        self.on_ending_tick()
        self.hero.effects.remove(self)

    def before_move_tick(self):
        pass

    def after_move_tick(self):
        pass

    def on_ending_tick(self):
        pass

    def __str__(self):
        return f"<{self.name} ({self.duration})>"


class Poisoning(Effect):
    name = 'Отравление'

    def __init__(self, hero, duration, damage):
        super().__init__(hero, duration)
        self.damage = damage

    def before_move_tick(self):
        print(f"{colors.CGREEN}Отравление в деле")
        self.hero.loose_hp(self.damage)
        print(colors.CEND, end='')
        self.decrease_duration()

    def __str__(self):
        return f"<{self.name} -|--- {self.damage} ({self.duration})>"


class Bleeding(Effect):
    name = 'Кровотечение'
    damage = 1

    def after_move_tick(self):
        print(f"{colors.CRED}У {self.hero.name} открытая рана")
        self.hero.loose_hp(self.damage)
        print(colors.CEND, end='')
        self.decrease_duration()


class Heeling(Effect):
    name = 'Лечение'

    def __init__(self, hero, duration, hill):
        super().__init__(hero, duration)
        self.hill = hill

    def before_move_tick(self):
        print(f"{colors.CBEIGE}лечение в деле")
        self.hero.regen_hp(self.hill)
        print(colors.CEND, end='')
        self.decrease_duration()

    def __str__(self):
        return f"<{self.name}++++ {self.hill} ({self.duration})>"


class Arson(Effect):
    name = "Поджог"

    def __init__(self, hero, duration):
        super().__init__(hero, duration)
        self.damage = 1

    def after_move_tick(self):
        print(f"{colors.CGREEN}Отравление в деле")
        self.hero.loose_hp(self.damage)
        print(colors.CEND, end='')
        self.decrease_duration()
        self.damage += 1


class Stun(Effect):
    name = 'Оглушение'

    def before_move_tick(self):
        self.hero.can_do_move = False
        self.decrease_duration()


class DelayedDamage(Effect):
    name = 'Отложенный урон'

    def __init__(self, hero, duration, damage, effects=[]):
        super().__init__(hero, duration)
        self.damage = damage
        self.effects = effects

    def after_move_tick(self):
        self.decrease_duration()

    def on_ending_tick(self):
        self.hero.loose_hp(self.damage)
        for effect in self.effects:
            self.hero.effects.append(effect)
