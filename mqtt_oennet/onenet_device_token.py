import base64
import hmac
import time
import hashlib
import ure
url = "mqtts.heclouds.com"
port = 1883

DeviceName = "stm32"  # 设备ID
Productid = "xsH8t9odKK"  # 产品ID
access_key = "V2JoNWh5bUpYQkw1dUVCdWx0dHVNMUV3Mmp2MVZXN0k="  # 秘钥

# 自定义 quote 函数，类似于 urllib.parse.quote
def my_quote(s, safe=''):
    """
    实现类似 urllib.parse.quote 功能的 URL 编码函数
    s: 要编码的字符串
    safe: 在编码时不进行编码的字符集合
    """
    # 默认保留字母数字和 safe 中的字符
    safe_chars = set(safe + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~")
    
    # 定义正则表达式，匹配非安全字符
    def encode(match):
        return f"%{ord(match.group(0)):02X}"
    
    # 使用正则替换所有非安全字符
    encoded = ure.sub(r'[^' + ''.join(safe_chars) + r']', encode, s)
    
    return encoded

def get_token(Productid,DeviceName,access_key,time):
    version = "2018-10-31"
    
    # 构造 API 路径
    res = "products/" + Productid + "/devices/" + DeviceName
    
    # 用户自定义 token 过期时间，设置为当前时间 + 10小时（36000000秒）
    et = str(1735971695 + 36000000)
    
    # 使用的签名方法
    method = "sha256"  # 选择 sha256 作为签名算法

    # 对 access_key 进行解码
    key = base64.b64decode(access_key)

    # 计算签名
    org = et + "\n" + method + "\n" + res + "\n" + version
    msg = org.encode()

    # 使用 hmac.new，传递哈希对象
    hmac_obj = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    sign_b = hmac_obj.digest()
    sign = base64.b64encode(sign_b).decode()
    print(f"org: {org}")
    print(f"sign_b: {sign_b}")
    print(f"sign: {sign}")

    # 对 sign 和 res 部分进行 URL 编码
    sign = my_quote(sign, safe='')
    res = my_quote(res, safe='')

    # 拼接 token 参数
    token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)

    return token

if __name__ == '__main__':
    token = get_token(Productid,DeviceName,access_key,time=1735971695)
    print(token)
