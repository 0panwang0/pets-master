import json


class Task:
    def __init__(self, task_num, info, money, exp, material_name, max_material, present_material, task_name):
        self.task_num = task_num
        self.info = info
        self.money = money
        self.exp = exp
        self.material_name = material_name
        self.max_material = max_material
        self.present_material = present_material
        self.task_name = task_name


def read_task(task_num):
    with open("resources\\task\\" + str(task_num), "r") as ob:
        info = json.load(ob)

    return Task(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])