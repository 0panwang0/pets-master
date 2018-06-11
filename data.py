from enum import Enum


class SkillType(Enum):
    NormalAttack = 0
    CatchPet = 1
    DirectDamage = 2
    AreaDamage = 3
    Heal = 4


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


class Skill:
    def __init__(self, skill_name, skill_type, skill_effort, skill_cost):
        self.skill_name = skill_name
        self.skill_type = skill_type
        self.skill_effort = skill_effort
        self.skill_cost = skill_cost


class Pet:
    def __init__(self, pet_name, pet_hp, pet_damage, pet_skill, pet_file, image_number=1):
        self.pet_name = pet_name
        self.pet_hp = pet_hp
        self.pet_hp_left = pet_hp
        self.pet_damage = pet_damage
        self.pet_skill = pet_skill
        self.pet_file = pet_file
        self.image_number = image_number

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


class Player:
    def __init__(self, name, hp, mp, damage, own_list, battle_list):
        self.name = name
        self.hp_total = hp
        self.hp_left = hp
        self.mp_total = mp
        self.mp_left = mp
        self.damage = damage
        self.own_list = own_list
        self.battle_list = battle_list

    def get_damage(self):
        return self.damage

    def get_skill_cost(self, index):
        return self.battle_list[index].get_skill().skill_cost

    def get_skill_type(self, index):
        return self.battle_list[index].get_skill().skill_type

    def get_skill_effort(self, index):
        return self.battle_list[index].get_skill().skill_effort

    def get_skill_available(self, index):
        return self.mp_left >= self.get_skill_cost(index)

    def get_skill_info(self, index):
        return self.get_skill_type(index), self.get_skill_effort(index), self.get_skill_cost(index)

    def use_skill(self, index):
        self.mp_left -= self.get_skill_cost(index)
        return self.get_skill_type(index), self.get_skill_effort(index), self.get_skill_cost(index)

    def take_damage(self, damage):
        self.hp_left -= damage
        if self.hp_left < 0:
            self.hp_left = 0

    def take_heal(self, heal):
        self.hp_left += heal
        if self.hp_left > self.hp_total:
            self.hp_left = self.hp_total

    def is_alive(self):
        return self.hp_left > 0
