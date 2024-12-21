import secrets
import hashlib
from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()
    save_key(key) 
    return key

def save_key(key):
    # 保存key到license文件
    with open('license', 'wb') as fw:
        fw.write(key)

def generate_aes_128_key():
    # 生成16字节（128位）的随机字节序列
    random_bytes = secrets.token_bytes(16)
    # 可以选择直接返回这16字节作为密钥（已经符合128位AES密钥长度要求）
    # return random_bytes
    # 或者为了增加随机性和安全性，再进行一次哈希处理（例如使用SHA256哈希）后取前16字节作为密钥
    hashed_key = hashlib.sha256(random_bytes).digest()[:16]
    with open('license_AES128', 'wb') as fw:
        fw.write(hashed_key)
    return hashed_key

def generate_aes_256_key():
    random_bytes = secrets.token_bytes(32)
    # 例如进行哈希处理（可选操作）
    hashed_key = hashlib.sha256(random_bytes).digest()[:32]
    with open('license_AES256', 'wb') as fw:
        fw.write(hashed_key)
    return hashed_key

