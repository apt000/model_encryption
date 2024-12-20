import io
import torch
from cryptography.fernet import Fernet
from generate_save_key import gen_key


def get_key(license_path):
    with open(license_path, 'rb') as fr:
        key = fr.read()
    return key

def model_encryption(model_path, encrypt_model_file, license_path):
    # step1: 读取pytorch模型，并转成io.Bytes
    model = torch.jit.load(model_path)
    buffer = io.BytesIO()
    torch.jit.save(model, buffer)  # Save to io.BytesIO buffer

    model.eval()  # 切换到评估模式
    buffer.seek(0)  # 这一句不能漏掉

    # step2：io.Bytes格式数据转成bytes格式数据
    pt_bytes = buffer.read()

    # step3：读取加密license获取密钥，进行加密
    key = get_key(license_path)
    # print(key) 
    encrypted_data = Fernet(key).encrypt(pt_bytes)

    # step4：保存加密文件
    with open(encrypt_model_file, 'wb') as fw:
        fw.write(encrypted_data)
    return encrypt_model_file

def model_decryption(encrypt_model_file, license_path):
    # step1：读取加密文件，得到加密的bytes格式数据
    with open(encrypt_model_file, 'rb') as fr:
        encrypted_data = fr.read()

    # step2：解密，得到解密后的bytes格式数据
    with open(license_path, 'rb') as fr:
        key = fr.read()
    decrypted_data = Fernet(key).decrypt(encrypted_data)

    # step3：解密后的bytes数据转成io.Bytes格式数据
    b = io.BytesIO(decrypted_data)
    b.seek(0)

    # step4：torch.load读取解密后的io.Bytes格式数据
    model = torch.jit.load(b)
    return model

def test_model(model):
    import torch.nn as nn
    import torch.optim as optim
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader

    # 超参数
    batch_size = 64

    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # 加载数据集
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    # 初始化模型、损失函数和优化器
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 测试模型
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"测试准确率: {100 * correct / total:.2f}%")

if __name__ == '__main__':
    gen_key()
    key = get_key('license')
    print(key)

    model_path = 'mnist_model.pt'
    encrypt_model_file = 'encrypt_model.pt'
    license_path = 'license'

    encrypt_model_path = model_encryption(model_path, encrypt_model_file, license_path)
    model = model_decryption(encrypt_model_path, license_path)
    test_model(model)

