import random

count = 0
for i in range(1000000):
    judge = random.randint(0, 10)
    count += 1
    while judge >= 5:
        count += 1
        judge = random.randint(0, 10)

print(count / 1000000)