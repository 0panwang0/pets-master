from enum import Enum


class BattleState(Enum):
    SelectAction = 0
    SelectEnermy = 1
    FriendRound = 2
    EnermyRound = 3
    EscapeJudge = 4


class BattleResult(Enum):
    Match = 0
    Victory = 1
    Defeat = 2
    Escape = 3


class SkillType(Enum):
    NormalAttack = 0
    CatchPet = 1
    DirectDamage = 2
    AreaDamage = 3
    Heal = 4


class Skill:
    def __init__(self, skill_name, skill_type, skill_effort, skill_cost):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.skill_effort = skill_effort
        self.skill_cost = skill_cost


class Pet:
    def __init__(self, pet_name, pet_hp, pet_damage, pet_skill, level, exp, beated_exp,
                 beated_money, pet_file, image_number=1):
        self.pet_name = pet_name
        self.pet_hp = pet_hp
        self.pet_hp_left = pet_hp
        self.pet_damage = pet_damage
        self.level = level
        self.pet_skill = pet_skill
        self.pet_file = pet_file
        self.image_number = image_number
        self.exp = exp
        self.beated_exp = beated_exp
        self.beated_money = beated_money
        self.exp_list = {
            1: 1000,
            2: 10000,
            3: 100000
        }

    def get_name(self):
        return self.pet_name

    def get_hp(self):
        return self.pet_hp_left

    def get_damage(self):
        return self.pet_damage

    def get_skill(self):
        return self.pet_skill

    def take_damage(self, damage):
        self.pet_hp_left -= damage
        if self.pet_hp_left < 0:
            self.pet_hp_left = 0

    def is_alive(self):
        return self.pet_hp_left > 0

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.exp_list[self.level]:
            print(self.pet_name, self.exp,  "level up!", self.exp_list[self.level])
        while self.exp >= self.exp_list[self.level]:
            self.level = self.level + 1
            self.exp -= self.exp_list[self.level]


