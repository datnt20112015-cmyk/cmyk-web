exp = 0

while True:
    print("\n=== GAME EXP ===")
    print("1. Danh quai nho (+10 EXP)")
    print("2. Danh quai lon (+30 EXP)")
    print("3. Xem EXP")
    print("4. Thoat")

    chon = input("Nhap lua chon: ")

    if chon == "1":
        exp += 10
        print("Ban da danh quai nho. +10 EXP")
    elif chon == "2":
        exp += 30
        print("Ban da danh quai lon. +30 EXP")
    elif chon == "3":
        print("EXP hien tai:", exp)
    elif chon == "4":
        print("Tam biet!")
        break