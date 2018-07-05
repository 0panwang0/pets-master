import pickle
import os
from pets import *


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