import pickle
import os
from pets import *
from task import *

# skill1 = Skill("爪击", SkillType.DirectDamage, 10, 5)
# skill2 = Skill("皮皮尤", SkillType.Heal, 20, 5)
# skill3 = Skill("尖刺针", SkillType.AreaDamage, 6, 7)
# enermy_pet1 = Pet("秋田犬", 13, 8, skill1, 1, 0, 25, 10,  "resources\\images\\Pets\\pet00.png", 18)
# enermy_pet2 = Pet("皮尤", 20, 4, skill2, 1, 0, 20, 10,  "resources\\images\\Pets\\pet01.png", 18)
# enermy_pet3 = Pet("仙人兽", 15, 6, skill3, 1, 0, 30, 10,  "resources\\images\\Pets\\pet02.png", 18)
# pets = [enermy_pet1, enermy_pet2, enermy_pet3]
#
# for num, pet in enumerate(pets):
#     pet_packet = pickle.dumps(pet)
#     with open(const.PETBIN_DIR + 'forest\\' + str(num) + '.bin', "wb") as object:
#         object.write(pet_packet)
#
# print(os.listdir('D:/pyCharm/procedures/pets-master/resources/pet/forest'))

# skill1 = Skill("翼击", SkillType.DirectDamage, 20, 10)
# skill2 = Skill("治愈花粉", SkillType.Heal, 40, 15)
# skill3 = Skill("冲撞", SkillType.AreaDamage, 13, 15)
# enermy_pet1 = Pet("小飞天", 20, 20, skill1, 15, 0, 50, 15,  "resources\\images\\Pets\\pet03.png", 18)
# enermy_pet2 = Pet("花纤纤", 35, 10, skill2, 15, 0, 55, 16,  "resources\\images\\Pets\\pet05.png", 18)
# enermy_pet3 = Pet("迪鲁", 23, 13, skill3, 15, 0, 60, 17,  "resources\\images\\Pets\\pet06.png", 18)
# pets = [enermy_pet1, enermy_pet2, enermy_pet3]
#
# for num, pet in enumerate(pets):
#     pet_packet = pickle.dumps(pet)
#     with open(const.PETBIN_DIR + 'forest1\\' + str(num) + '.bin', "wb") as object:
#         object.write(pet_packet)
#
# print(os.listdir('D:/pyCharm/procedures/pets-master/resources/pet/forest1'))

skill1 = Skill("地狱拳", SkillType.DirectDamage, 50, 10)
skill2 = Skill("地狱若水", SkillType.Heal, 100, 15)
skill3 = Skill("地狱无敌轰", SkillType.AreaDamage, 30, 20)
enermy_pet1 = Pet("冥伽", 150, 58, skill1, 30, 0, 250, 63,  "resources\\images\\Pets\\pet04.png", 18)
enermy_pet2 = Pet("浮幽", 200, 40, skill2, 30, 0, 200, 78,  "resources\\images\\Pets\\pet07.png", 18)
enermy_pet3 = Pet("奜", 100, 100, skill3, 30, 0, 300, 100,  "resources\\images\\Pets\\pet10.png", 18)
pets = [enermy_pet1, enermy_pet2, enermy_pet3]

for num, pet in enumerate(pets):
    pet_packet = pickle.dumps(pet)
    with open(const.PETBIN_DIR + 'rocks\\' + str(num) + '.bin', "wb") as object:
        object.write(pet_packet)

print(os.listdir('D:/pyCharm/procedures/pets-master/resources/pet/rocks'))

# task = Task(1, [ "秋田犬又在肆虐家园了，", "快去剿灭它们吧！"], 100, 1000, "秋田犬", 5, 0, "秋田犬之殇")
# task_packet = pickle.dumps(task)
#
# with open("resources\\task\\1.bin", "wb") as object:
#     object.write(task_packet)
#
# task = Task(2, [ "仙人刺可以作成织毛衣的针呢，", "快去收集一些吧！"], 100, 1000, "仙人兽", 10, 0, "缝缝补补")
# task_packet = pickle.dumps(task)
#
# with open("resources\\task\\2.bin", "wb") as object:
#     object.write(task_packet)
#
# task = Task(3, ["皮尤可以松土哦，捉一些给菜园子", "里的那个家伙，他肯定很高兴的。"], 100, 1000, "皮尤", 2, 0, "可怜的皮尤")
# task_packet = pickle.dumps(task)
#
# with open("resources\\task\\3.bin", "wb") as object:
#     object.write(task_packet)
#
# task = Task(4, [ "女孩子很喜欢可爱的宠物呢，", "你一定也想捉一些作为礼物吧？"], 200, 5000, "小飞天", 3, 0, "宠物真的可爱吗？")
# task_packet = pickle.dumps(task)
#
# with open("resources\\task\\4.bin", "wb") as object:
#     object.write(task_packet)
#
# print(os.listdir('D:\pyCharm\procedures\pets-master\\resources\\task'))
