from math import lcm

# Tổng số cây mỗi đội trồng là như nhau
# Đội I: 7 cây/người, Đội II: 8 cây/người, Đội III: 6 cây/người
# Gọi số cây chung là S, ta có: S chia hết cho 7, 8, 6.
# S phải nằm trong khoảng 100 đến 200.

S = None
for x in range(100, 201):
    if x % 7 == 0 and x % 8 == 0 and x % 6 == 0:
        S = x
        break

if S is None:
    print("Không có số cây chung nào từ 100 đến 200 thỏa mãn.")
else:
    so_cong_nhan_doi_I = S // 7
    so_cong_nhan_doi_II = S // 8
    so_cong_nhan_doi_III = S // 6

    print(f"Số cây mỗi đội trồng là: {S}")
    print(f"Đội I: {so_cong_nhan_doi_I} công nhân")
    print(f"Đội II: {so_cong_nhan_doi_II} công nhân")
    print(f"Đội III: {so_cong_nhan_doi_III} công nhân")
