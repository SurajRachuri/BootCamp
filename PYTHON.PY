# 33110
# 33870
# 33300
# 33710
# 32250
# 34250
# 30120
# 33800
# 33990
# 31530
# 33260
# 33470
# 34240
# 33560
# 34060
# 34320
# 34010
# 34330
# Print 3 Numbers whose total is 101260

numbers = [33110, 33870, 33300, 33710, 32250, 34250, 30120, 33800, 33990, 31530, 33260, 33470, 34240, 33560, 34060, 34320, 34010, 34330]
t = 101260

for i in range(len(numbers)):
    for j in range(i+1, len(numbers)):
        for k in range(j+1, len(numbers)):
            if numbers[i] + numbers[j] + numbers[k] == t:
                print(f"{numbers[i]} + {numbers[j]} + {numbers[k]} = {t}")
            continue