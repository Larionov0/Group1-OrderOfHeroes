
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
        delayed = effects.DelayedHeeling(team_mate, 2, 10)
        team_mate.effects.append(delayed)
        self.did_action = True

    def cast_2_skill(self, my_team, enemies_team):
        enemy = self.choose_hero_from_list(enemies_team)
        if enemy is False:
            return
        cycles = effects.Silence(enemy, 1)
        enemy.effects.append(cycles)
        self.did_action = True
