import pickle
import os
from pets import *
from task import *

skill1 = Skill("地狱拳", SkillType.DirectDamage, 50, 10)
skill2 = Skill("地狱若水", SkillType.Heal, 100, 15)
skill3 = Skill("地狱无敌轰", SkillType.AreaDamage, 30, 20)
enermy_pet1 = Pet("冥伽", 150, 58, skill1, 1, 0, 250, 63,  "resources\\images\\Pets\\pet04.png", 18)
enermy_pet2 = Pet("浮幽", 200, 40, skill2, 1, 0, 200, 78,  "resources\\images\\Pets\\pet07.png", 18)
enermy_pet3 = Pet("奜", 100, 100, skill3, 1, 0, 300, 100,  "resources\\images\\Pets\\pet10.png", 18)
pets = [enermy_pet1, enermy_pet2, enermy_pet3]

for num, pet in enumerate(pets):
    pet_packet = pickle.dumps(pet)
    with open(const.PETBIN_DIR + 'rocks\\' + str(num) + '.bin', "wb") as object:
        object.write(pet_packet)

print(os.listdir('D:/pyCharm/procedures/pets-master/resources/pet/forest'))

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
