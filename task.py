class Task:
    def __init__(self, task_num, type, money, exp, material_name, task_name, max_material, present_material):
        self.task_num = task_num
        self.type = type   # 任务类型 1.击杀怪物，2.获取材料，3.跑腿(传话)，4抓捕怪物
        self.money = money
        self.exp = exp
        self.material_name = material_name
        self.max_material = max_material
        self.present_material = present_material
        self.task_name = task_name