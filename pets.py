from enum import Enum
import const
from math import *

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
        self.lvup_exp = floor(pow((self.level + 1), const.DOD) * 100 + pow(self.level, 1 / const.DOD) * 100)

    def save(self):
        list = []
        skill_type = 0
        for i in range(5):
            if self.pet_skill.skill_type.value == i:
                skill_type = i
                break
        skill = [self.pet_skill.skill_name, skill_type, self.pet_skill.skill_effort, self.pet_skill.skill_cost]
        list.append(self.pet_name)
        list.append(self.pet_hp)
        list.append(self.pet_damage)
        list.append(skill)
        list.append(self.level)
        list.append(self.exp)
        list.append(self.beated_exp)
        list.append(self.beated_money)
        list.append(self.pet_file)
        list.append(self.image_number)
        list.append(self.pet_hp_left)

        return list

    def load(self, list):
        self.pet_hp_left = list[-1]

    def get_name(self):
        return self.pet_name

    def get_hp(self):
        return self.pet_hp_left

    def get_damage(self):
        return self.pet_damage

    def get_skill(self):
        return self.pet_skill

    def get_effort(self):
        return int(self.pet_skill.skill_effort * (0.8 + 0.2 * self.level))

    def take_damage(self, damage):
        self.pet_hp_left -= damage
        if self.pet_hp_left < 0:
            self.pet_hp_left = 0

    def is_alive(self):
        return self.pet_hp_left > 0

    def gain_exp(self, exp):
        self.exp += exp
        if self.exp >= self.lvup_exp:
            while self.exp >= self.lvup_exp:
                self.level = self.level + 1
                self.exp -= self.lvup_exp
                self.lvup_exp = floor(pow((self.level + 1), const.DOD) * 100 + pow(self.level, 1 / const.DOD) * 100)
            return True
        else:
            return False
