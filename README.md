# model_encryption
## 使用cryptography库
```
from cryptography.fernet import Fernet
```
**加密过程**：
1. 先将模型转换成io.Bytes
2. io.Bytes格式数据转成bytes格式数据  
3. 获取秘钥利用cryptography.fernet进行加密
4. 保存加密文件<br>

**解密过程**：
1. 读取加密文件，得到加密的bytes格式数据  
2. 获取秘钥进行解密  
3. 解密后的bytes数据转成io.Bytes格式数据  
4. 读取解密后的文件<br>

## AES对称加密
https://mp.weixin.qq.com/s/sKvQLtf44fW6Dp4GIb0Y4g?token=75639845&lang=zh_CN
```
pip install PyCryptodome
```
```
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
```
**加密过程**：
1. 密钥生成：生成一个 16 字节（128 位）、24 字节（192 位）或 32 字节（256 位）的随机密钥
2. 初始化向量生成：生成一个与密钥长度相同的随机初始化向量（IV）。IV 用于增加加密的随机性，防止相同明文加密后得到相同的密文。
3. 创建 AES 加密对象：使用生成的密钥和选定的加密模式创建 AES 加密对象。常见的加密模式有 ECB（电子密码本模式）、CBC（密码分组链接模式）、CFB（密文反馈模式）、OFB（输出反馈模式）等。这里使用了CBC。
4. 填充明文：如果明文长度不是加密块大小的整数倍，需要对明文进行填充。这里使用 PKCS7 填充。
5. 加密操作：使用创建的加密对象对填充后的明文进行加密，得到密文对模型进行加密。

**解密过程**：
1. 读取密钥和初始化向量：从存储介质（如文件、数据库等）中读取加密时使用的密钥和初始化向量。 
2. 创建 AES 解密对象：使用读取的密钥和初始化向量以及与加密时相同的加密模式创建 AES 解密对象。
3. 解密操作：使用解密对象对密文进行解密，得到填充后的明文。  
4. 去除填充：对解密后的填充明文进行去除填充操作，得到原始明文和解密后的模型文件。<br>
