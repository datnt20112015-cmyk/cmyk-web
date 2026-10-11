xu = 100
binh_mau = 0

while True:
    print("\n===== TÚI ĐỒ =====")
    print("1. Xem túi đồ")
    print("2. Nhặt bình máu")
    print("3. Sử dụng bình máu")
    print("4. Bán vật phẩm")
    print("0. Thoát")

    chon = input("Chon: ")

    if chon == "1":
        print("Xu hien tai:", xu)
        print("So bình máu:", binh_mau)
    elif chon == "2":
        if xu >= 20:
            xu -= 20
            binh_mau += 1
            print("Bạn đã nhặt 1 bình máu.")
        else:
            print("Không đủ xu để nhặt bình máu.")
    elif chon == "3":
        if binh_mau > 0:
            binh_mau -= 1
            print("Bạn đã sử dụng 1 bình máu.")
        else:
            print("Bạn không có bình máu.")
    elif chon == "4":
        xu += 10
        print("Bạn đã bán vật phẩm và nhận được 10 xu.")
    elif chon == "0":
        print("Thoát game.")
        break
    else:
        print("Lựa chọn không hợp lệ.")
