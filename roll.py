import random
a = int(input("a: "))
b = int(input("b: "))
if a>b:a,b=b,a
so_bi_mat = random.randint(a + 1, b - 1)
n = int(input("Nhap so: "))
while n !=so_bi_mat:
    if n< so_bi_mat: print("Sai, lon hon")
    else:print("Sai, nho hon")
    n =int(input("Nhap lai: "))
print("Dung roi")