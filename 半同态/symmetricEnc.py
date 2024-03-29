from phe import paillier  # 开源库
from Crypto.Cipher import AES
import random  # 选择随机数

##################### 设置参数
# 服务器端保存的数值
plaintext_list = [
    b'0123456789abcdef',
    b'qwertyuiopasdfgh',
    b'------nku-------',
    b'thisisalabreport',
    b'**chenruiying** '
]
ciphertext_list = []
ciphernum_list = []
symmetric_key = b'------nku-------'
aes = AES.new(symmetric_key, AES.MODE_ECB)  # 创建一个aes对象
for text in plaintext_list:
    ciphertext_list.append(aes.encrypt(text))  # 加密明文
    ciphernum_list.append(int.from_bytes(text, byteorder='big'))

for element in ciphertext_list:
    print(element)

length = len(ciphertext_list)
# 客户端生成公私钥
public_key, private_key = paillier.generate_paillier_keypair()
# 客户端随机选择一个要读的位置
pos = random.randint(0, length - 1)
print("要读起的数值位置为：", pos)

##################### 客户端生成密文选择向量
select_list = []
enc_list = []
for i in range(length):
    select_list.append(i == pos)
    enc_list.append(public_key.encrypt(select_list[i]))

for element in select_list:
    print(element)
for element in enc_list:
    print(element)
for element in enc_list:
    print(private_key.decrypt(element))

##################### 服务器端进行运算
c = 0
for i in range(length):
    c = c + ciphernum_list[i] * enc_list[i]
print("产生密文：", c.ciphertext())

##################### 客户端进行解密
m = private_key.decrypt(c)
print("得到数值：", m)

message = m.to_bytes(16, byteorder='big')
x = aes.decrypt(message)
print(message)
