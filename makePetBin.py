import pickle
import os
from pets import *


skill1 = Skill("霸王拳", SkillType.DirectDamage, 6, 5)
skill2 = Skill("霸王若水", SkillType.Heal, 10, 5)
skill3 = Skill("霸王无敌轰", SkillType.AreaDamage, 5, 10)
enermy_pet1 = Pet("秋田犬", 20, 5, skill1, 1, 20, 500, 20,  "resources\\images\\Pets\\pet00.png", 18)
enermy_pet2 = Pet("皮尤", 20, 5, skill2, 1, 20, 500, 20,  "resources\\images\\Pets\\pet01.png", 18)
enermy_pet3 = Pet("仙人兽", 20, 5, skill3, 1, 20, 500, 20,  "resources\\images\\Pets\\pet02.png", 18)
enermy_pet4 = Pet("小飞天", 20, 5, skill1, 1, 20, 500, 20,  "resources\\images\\Pets\\pet03.png", 18)
enermy_pet5 = Pet("冥伽", 20, 5, skill2, 1, 20, 500, 20,  "resources\\images\\Pets\\pet04.png", 18)
enermy_pet6 = Pet("花纤纤", 20, 5, skill3, 1, 20, 500, 20,  "resources\\images\\Pets\\pet05.png", 18)
enermy_pet7 = Pet("迪鲁", 20, 5, skill1, 1, 20, 500, 20,  "resources\\images\\Pets\\pet06.png", 18)
pets = [enermy_pet1, enermy_pet2, enermy_pet3, enermy_pet4, enermy_pet5, enermy_pet6, enermy_pet7]

for num, pet in enumerate(pets):
    pet_packet = pickle.dumps(pet)
    with open(const.PETBIN_DIR + 'forest\\' + str(num) + '.bin', "wb") as object:
        object.write(pet_packet)

print(os.listdir('D:/pyCharm/procedures/pets-master/resources/pet_bin/forest'))