from enum import Enum


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
    def __init__(self, pet_name, pet_hp, pet_damage, pet_skill, level, exp, pet_file, image_number=1):
        self.pet_name = pet_name
        self.pet_hp = pet_hp
        self.pet_hp_left = pet_hp
        self.pet_damage = pet_damage
        self.pet_skill = pet_skill
        self.pet_skill.skill_name += '(' + self.level + ')'
        self.pet_file = pet_file
        self.image_number = image_number
        self.level = level
        self.exp = exp
        self.exp_list = {
            '1': 1000,
            '2': 10000,
            '3': 100000
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

    def up_level(self):
        for level, exp in self.exp_list:
            if self.exp > exp and self.level < level:
                self.level = level
                # 提示升级了
                self.pet_skill.skill_effort = int(self.level) * 10 # 增加攻击力
                self.pet_skill.skill_name = self.pet_skill.skill_name[:-3] + '(' + self.level + ')'