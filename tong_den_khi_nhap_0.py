#bai6
'''
exp = 0
while True:
    print("1. quai nho (+10)\n2. quai lon (+30)\n3. xem EXP\n4. thoat")
    ch = input("Chon: ")
    if ch== "1": exp += 10
    elif ch == "2": exp += 30
    elif ch=="3": print("EXP:", exp)
    elif ch== "4": break
    if exp >=100: print("Len cap")
'''
#bai7
'''
xu = 100
binh = 0
while True:
    print("1.xem\n2.nhat\n3.dung\n4.ban\n0.thoat")
    ch = input("Chon: ")
    if ch == "1": print("xu:", xu, "binh:", binh)
    elif ch == "2":
        if xu >= 20: xu -= 20; binh += 1
        else: print("Khong du xu")
    elif ch == "3":
        if binh > 0: binh -= 1
        else: print("Khong co binh")
    elif ch == "4": xu += 10
    elif ch == "0": break
'''
