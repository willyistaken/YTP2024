my_list = [120, 120, 800, 200, 300]

for i in reversed(range(len(my_list))):
    if my_list[i]>100:
        del my_list[i]
print(my_list)