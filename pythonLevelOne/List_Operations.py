def ListSum(n: list):
    sum=0
    for i in range(0, len(n)):
        sum += n[i]
    return sum
 
def AvgList(n: list):
    sum = ListSum(n)
    avg = sum/len(n)
    return avg
 
def MaxList(n: list):
    max=0
    for i in range(0,len(n)):
        if n[i]> max:
            max= n[i]
    return max
 
def MinList(n: list):
    min=n[0]
    for i in range(0,len(n)):
        if n[i]< min:
            min= n[i]
    return min
 
def RevList(n: list):
    rev=[]
    for i in range(len(n)-1, -1, -1):
        rev.append(n[i])
    return rev
 
n = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
sum = ListSum(n)
print(f"Sum of the List: {sum}")
print("--------")
 
avg=AvgList(n)
print(f"Average of List: {avg}")
print("--------")
 
max=MaxList(n)
print(f"Maximum Value in List: {max}")
print("--------")
 
min=MinList(n)
print(f"Minimum Value in List: {min}")
print("--------")
 
rev=RevList(n)
print(f"Reverse order of List:")
for num in rev:
    print(num)
print("--------")

from OPPS.Attributes_Methods import test

test()