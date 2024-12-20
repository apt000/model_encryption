from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()
    save_key(key) 


def save_key(key):
    # 保存key到license文件
    with open('license', 'wb') as fw:
        fw.write(key)
