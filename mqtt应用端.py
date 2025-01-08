import base64
import hmac
import time
from urllib.parse import quote
import requests
import json
# 用户ID(用户头像->访问权限->user_id)
user_id = '401337'
# 访问密钥(用户头像->访问权限->access_key)
access_key = "RneHqQ12ZCzERs+AFB1A3ZxcTqxPvrjAiCRumsSunMCK9+4DZD/jqShWGRvkiWXUOOM06Eno6xStBMl4z9zxrg=="
#产品id(产品->产品ID)
product_id = "xsH8t9odKK"
#设备名称
device_name = "stm32"
class OneNet():
    def __init__(self,user_id, access_key,product_id,device_name):
        self.user_id = user_id
        self.access_key = access_key
        self.product_id = product_id
        self.device_name = device_name
        self.token = self.get_token()
        pass
    
    def get_token(self):
        version = '2022-05-01'
        res = 'userid/%s' % self.user_id
        # 用户自定义token过期时间
        et = str(int(time.time()) + 3600000)
        # 签名方法，支持md5、sha1、sha256
        method = 'sha1'
        # 对access_key进行decode
        key = base64.b64decode(self.access_key)
        # 计算sign
        org = et + '\n' + method + '\n' + res + '\n' + version
        sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
        sign = base64.b64encode(sign_b.digest()).decode()
        # value 部分进行url编码，method/res/version值较为简单无需编码
        sign = quote(sign, safe='')
        res = quote(res, safe='')
        # token参数拼接
        token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)
        return token
    
    def Get_Platform_DiveceData(self):     
        """_summary_
            获取平台设备数据
            返回字典类型数据
        """
        headers ={
            "authorization": f"{self.token}"
        }
        url = f"http://iot-api.heclouds.com/thingmodel/query-device-property?product_id={self.product_id}&device_name={self.device_name}"
        response = requests.get(url,headers=headers)
        return response.json()
    def Get_DiveceData(self,attribute,timeout=3):
        """_summary_
        直接向设备获取数据
        对应设备侧：
            平台获取直连设备的属性(用户直接向设备发送读取数值请求,对应获取设备属性详情api)设备需要订阅的topic如下
            $sys/xsH8t9odKK/stm32/thing/property/get  订阅
            {"id":"106","version":"1.0","params":["led","brightness"]} 这里注意有列表
            直连设备回复平台获取设备属性（设备直接向用户回复）
            $sys/xsH8t9odKK/stm32/thing/property/get_reply 发布 示例代码如下
            {
                "id":"102",
                "code":200,
                "msg":"succ",
                "data":{
                    "led":true,
                    "brightness":20
                }
            }
            id号必须匹配,code必须200,其他任意
        Args:
            attribute (list): 查找属性的列表例：["brightness","led"]
            timeout (int, optional): 超时时间. Defaults to 3.
            Returns:state_succ_code = 0
                    state_fail_code = 1
        """
        state_succ_code = 0
        state_fail_code = 1
        url = "http://iot-api.heclouds.com/thingmodel/query-device-property-detail"
        headers ={
            "Content-Type": "application/json",
            "authorization": f"{self.token}",
        }
        js_data = {
        "product_id":f"{self.product_id}",
        "device_name":f"{self.device_name}",
        "params": []
        }
        js_data["params"]=attribute
        
        try:
            response = requests.post(url, headers=headers, json=js_data, timeout=timeout)  # 设置 10 秒超时
            response.raise_for_status()  # 如果响应状态码不是 2xx，会抛出异常
            if response.json()["msg"] == "succ":
                print("获取成功")
                return state_succ_code,response.json()
                
        except requests.exceptions.Timeout:
             error_msg = "请求超时，设备响应可能超时或网络问题。"
             print(error_msg)  # 超时处理
             return state_fail_code, error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"请求失败: {e}"
            print(error_msg)
            return state_fail_code, error_msg 
    def Set_DiveceData(self,data,timeout=3):
        """_summary_
        设置设备数据
        对应设备侧：
        
            设置设备属性(用户直接控制设备,对应的设置属性api)设备需要订阅的topic如下
            $sys/xsH8t9odKK/{device-name}/thing/property/set   订阅 
            收到的示例代码如下
            {"id":"105","version":"1.0","params":{"brightness":20,"led":false}}
            设置直连设备属性（设备回复设置成功）
            $sys/xsH8t9odKK/{device-name}/thing/property/set_reply   发布 
            示例代码如下
            {
                "id": "30",
                "code": 200,
                "msg": "succ"
            }id号需要匹配用户发来的id号,code必须200其他无所谓,msg必须为succ才算成功
        Args:
            data (dict): 设置属性的字典例：{"brightness":30,"led":False}
            timeout (int, optional): 超时时间. Defaults to 3.
            Returns:state_succ_code = 0
                    state_fail_code = 1
        """
        state_succ_code = 0
        state_fail_code = 1
        js_data = {
        "product_id":f"{self.product_id}",
        "device_name":f"{self.device_name}",
        "params": {
            
        }
        }
        headers ={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "authorization": f"{self.token}",
        }
        url = "http://iot-api.heclouds.com/thingmodel/set-device-property"
        js_data["params"].update(data)
        
        try:
            response = requests.post(url, headers=headers, json=js_data, timeout=timeout)  # 设置 10 秒超时
            response.raise_for_status()  # 如果响应状态码不是 2xx，会抛出异常
            if response.json()["msg"] == "succ":
                print("设置成功")
                print("响应内容：", response.json())  # 打印响应的 JSON 数据
                return state_succ_code
                
        except requests.exceptions.Timeout:
            print("请求超时，设备响应可能超时或网络问题。")  # 超时处理
            return state_fail_code
            
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return state_fail_code
                
        
if __name__ == '__main__':
    client  = OneNet(user_id, access_key,product_id,device_name)
    # while True:
    #     data = client.Get_Platform_DiveceData()
        
    #     print("获取平台设备数据成功：",data)
    #     time.sleep(3)
    attribute = ["led","brightness"]
    data = {"led":True,"brightness":30}
    # state_code = 1
    # while state_code == 1:
    #     state_code,device_data = client.Get_DiveceData(attribute)
    #     time.sleep(1)
    # print("获取设备数据成功：",device_data)
    state_code = 1
    while state_code:
        state_code = client.Set_DiveceData(data)
        time.sleep(1)
    print("测试完成")