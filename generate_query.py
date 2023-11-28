import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))


arr = []
str = ""

for i in range(109):
    for j in range(25):
        str_rand = get_random_string(15)
        if str_rand not in arr:
            str += f"INSERT INTO tb_KhoHang(MaCTHDNhap, IMEI) VALUES({i + 1}, '{str_rand}')\n"
            arr.append(str_rand)

print(str)
