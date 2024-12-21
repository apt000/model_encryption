# pip install PyCryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import torch
from model_encrypt import test_model
from generate_save_key import generate_aes_256_key

def encrypt_model(model_path, encrypt_model_file):
    key = generate_aes_256_key()
    with open(model_path, 'rb') as f:
        model_data = f.read()
    # 使用AES进行加密
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_model = cipher.encrypt(pad(model_data, AES.block_size))
    with open(encrypt_model_file, 'wb') as f:
        f.write(cipher.iv)  # IV在解密时使用
        f.write(encrypted_model)
    return encrypt_model_file
    
def decrypt_model(encrypt_model_file, decrypt_model_file, license_path):
    with open(encrypt_model_file, 'rb') as f:
        iv = f.read(16)  # 读取前16字节的IV
        encrypted_model = f.read()  # 读取加密后的模型数据

    with open(license_path, 'rb') as fr:
        key = fr.read()
    # 使用AES进行解密
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_model = unpad(cipher.decrypt(encrypted_model), AES.block_size)
    with open(decrypt_model_file, 'wb') as f:
        f.write(decrypted_model)
    model = torch.jit.load(decrypt_model_file)

    return model
    

if __name__ == "__main__":
    model_path = 'mnist_model.pt'
    encrypt_model_file = 'encrypt_AES_model.pt'
    decrypt_model_file = 'mnist_model_decry.pt'
    license_path = 'license_AES256'

    encrypt_model(model_path, encrypt_model_file)
    model = decrypt_model(encrypt_model_file, decrypt_model_file, license_path)

    test_model(model)

