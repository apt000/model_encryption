# model_encryption
## 使用cryptography库
`from cryptography.fernet import Fernet`  
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


