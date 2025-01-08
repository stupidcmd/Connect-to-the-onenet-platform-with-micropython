import onenet_device_token
from  umqtt.robust import MQTTClient
from  wifi_connect import wifi
import time
import random
import  json
import uasyncio
from ledtest import led_on,led_off
from machine import Pin
replay_msg = None
replay_state_code = None
token = None

ssid = "405"
password = "15980997653"

url = "mqtts.heclouds.com"
port = 1883

DeviceName = "stm32"  # 设备ID
Productid = "xsH8t9odKK"  # 产品ID
access_key = "dlZZcTBYVkF4emwyRElrTXJoVENvNlBHY3cwdVE1ajI="  # 秘钥




def main():
    global replay_msg 
    global replay_state_code 
    token = onenet_device_token.get_token(Productid,DeviceName,access_key,time=1735971695)
    print(token)
    wlan = wifi(ssid = ssid,password = password)
    client = ONENET(client_id=DeviceName,server=url,port=port,user=Productid,keepalive=100,password=token)
    #设置回调函数(必须要)
    client.client.set_callback(on_message)
    
    client.Subscribe_topic(post_replay_topic="$sys/xsH8t9odKK/stm32/thing/property/post/reply")
    client.Subscribe_topic(set_topic = "$sys/xsH8t9odKK/stm32/thing/property/set")
    client.Subscribe_topic(get_topic = "$sys/xsH8t9odKK/stm32/thing/property/get")
    
    uasyncio.run(creat_tasks(client))
    
#     client.Post_Data(brightness=get_sensor_data(),led=get_led_state())
    
#     try:
#         while True:
#             
#             client.client.check_msg()  # 检查是否有新的消息
#             # 你可以在这里执行其他操作，例如读取传感器数据等
#             print("Performing other tasks...")
#             if replay_state_code == "reply":
#                 print("Post success")
#                 replay_state_code = None
# #                 break
#             if replay_state_code =="set":
#                 wait_handle_msg = replay_msg
#                 replay_id = wait_handle_msg["id"]
#                 client.Set_replay(replay_id)
#                 params = wait_handle_msg.get("params", {})
#                 for key,value in params.items():
#                     if key =="led":
#                         print("+++++++++++++++++++++++++++++++++++++")
#                 replay_msg = None
#                 replay_state_code = None
# #                 break
#             if replay_state_code == "get":
#                 wait_replay_msg = replay_msg
#                 get_replay_id = wait_replay_msg["id"]
#                 data={}
#                 for params in wait_replay_msg["params"]:
#                     if params=="brightness":
#                         data[params] = get_sensor_data()
#                     if params=="led":
#                         data[params] = get_led_state()
# #                 print(data)
#                 client.Get_replay(get_replay_id,data)
#                 print("Data has post to client")
# #                 print(data)
#                 replay_msg = None
#                 replay_state_code = None
#                     
#                     
#             time.sleep(1) 
#     except KeyboardInterrupt:
#         print("MQTT subscription stopped.")
#     finally:
#         client.client.disconnect()
    
class ONENET():
    posts_data ={
    "id": "123",
    "version": "1.0",
    "params": {}
                }
    set_replay ={
        "id": "30",
        "code": 200,
        "msg": "succ"
                }
    get_replay = {
    "id":"102",
    "code":200,
    "msg":"succ",
    "data":{
        
        }
    }
        
#     post_topic = f"$sys/{Productid}/{DeviceName}/thing/property/post" pub
#     post_replay_topic =f"$sys/{Productid}/{DeviceName}/thing/property/post/reply" sub
#	  set_topic = "$sys/{Productid}/{DeviceName}/thing/property/set" sub
#     set_replay_topic = "$sys/{Productid}/{DeviceName}/thing/property/set_reply" pub
#     get_topic = "$sys/{Productid}/{DeviceName}/thing/property/get" sub
#     get_replay_topic = f"$sys/{Productid}/{DeviceName}/thing/property/get_reply" pub
#======================================================================================
#作者:trashedmaker
#开源文件,未注明请勿转载
#原文链接:https://blog.csdn.net/m0_73949172/article/details/144929662?spm=1001.2014.3001.5501
#======================================================================================
    def __init__(self,client_id,server,port,user,keepalive,password):
        self.client_id = client_id
        self.server = server
        self.port = port
        self.user = user
        self.keepalive = keepalive
        self.password = password
        self.client =self.connect_mqtt(self.password)
        self.id = None
        self.post_topic = f"$sys/{user}/{client_id}/thing/property/post"
        self.set_replay_topic = f"$sys/{user}/{client_id}/thing/property/set_reply"
        self.get_replay_topic = f"$sys/{user}/{client_id}/thing/property/get_reply"
        
        
    def connect_mqtt(self,token):
        client = MQTTClient(client_id=self.client_id,server=self.server,port=self.port,user=self.user,keepalive=self.keepalive,password=self.password)
        while 1:
            
            try:
                client.connect()
                print('Has Connected to OneNET')
                break
#             0	CONNECTION_ACCEPTED - 连接成功
#             1	CONNECTION_REFUSED_PROTOCOL_VERSION - 版本号错误
#             2	CONNECTION_REFUSED_IDENTIFIER_REJECTED - 连接标识符被拒绝
#             3	CONNECTION_REFUSED_SERVER_UNAVAILABLE - 服务器不可用
#             4	CONNECTION_REFUSED_BAD_USER_NAME_OR_PASSWORD - 错误的用户名或密码
#             5	CONNECTION_REFUSED_NOT_AUTHORIZED - 没有权限
            except Exception as e:  # 捕获所有异常
                print(f"Something went wrong: Wrong code is {e}")  # 打印错误信息
                print("We are trying again...")
                time.sleep(1)  # 等待 1 秒后重新尝试连接
            
        return client
    
    async def Post_Data(self,**kwargs):
    
        data = self.posts_data
        data["id"] = str(random.randint(1,1000))
        self.id = data["id"]
        for key,value in kwargs.items():
            data["params"][key] = {"value":value}
        self.client.publish(self.post_topic,json.dumps(data))
        print(data)
        
    def Subscribe_topic(self,**kwargs):
        for sub_topic,sub_topic_value in kwargs.items():
            try:
                self.client.subscribe(sub_topic_value)
                print(f"Subscribed to {sub_topic}")
            except:
                print(f"Faile Subscribed to {sub_topic}!!!!")
        pass
    async def Set_replay(self,msg_id):
        data = self.set_replay
        data["id"] = msg_id
        data = json.dumps(data)
        self.client.publish(self.set_replay_topic,data)
        print(data)
    async def Get_replay(self,msg_id,replay_data):
        data = self.get_replay
        data["id"]=msg_id
        data["data"]=replay_data
        data = json.dumps(data)
        self.client.publish(self.get_replay_topic,data)
        print(data)
        pass
        
        
    #回复的消息topic和msg都是b""需要decode一下
def on_message(topic, msg):
    topic = topic.decode('utf-8')
    msg = json.loads(msg.decode('utf-8'))
    global replay_msg
    global replay_state_code
    topic = topic.split("/")[-1]
    if topic == "reply":
        if msg["msg"] == "success":
            replay_state_code = topic

    if topic == "set":
        replay_state_code = topic
        replay_msg = msg
    if topic == "get":
        replay_state_code = topic
        replay_msg = msg
    print(msg)
def get_sensor_data():
    data = random.randint(0,100)
    return data
def get_led_state():
    data = random.randint(0,1)
    if data == 1:
        return True
    else:
        return False
async def Regularly_upload_data(client,time):
    while 1:
        await client.Post_Data(brightness=get_sensor_data(),led=get_led_state())
        await uasyncio.sleep(time);   
    pass
async def Regularly_hanle_msg(client,time):
    global replay_state_code
    global replay_msg
    p40 = Pin(40,Pin.OUT)
    try:
        while True:
            
            client.client.check_msg()  # 检查是否有新的消息
            # 你可以在这里执行其他操作，例如读取传感器数据等
            if replay_state_code == "reply":
                print("Post success")
                replay_state_code = None
#                 break
            if replay_state_code =="set":
                wait_handle_msg = replay_msg
                replay_id = wait_handle_msg["id"]
                await client.Set_replay(replay_id)
                params = wait_handle_msg.get("params", {})
                for key,value in params.items():
                    if key =="led":
                        if value == 1:
                            led_on(p40)
                        else:
                            led_off(p40)
                            
                        
                replay_msg = None
                replay_state_code = None
#                 break
            if replay_state_code == "get":
                wait_replay_msg = replay_msg
                get_replay_id = wait_replay_msg["id"]
                data={}
                for params in wait_replay_msg["params"]:
                    if params=="brightness":
                        data[params] = get_sensor_data()
                    if params=="led":
                        data[params] = get_led_state()
#                 print(data)
                await client.Get_replay(get_replay_id,data)
                print("Data has post to client")
#                 print(data)
                replay_msg = None
                replay_state_code = None
                    
                    
            await uasyncio.sleep(time) 
    except KeyboardInterrupt:
        print("MQTT subscription stopped.")
    finally:
        client.client.disconnect()
    pass
async def creat_tasks(client):
    tasks = []
    t1 = uasyncio.create_task(Regularly_upload_data(client,3))
    t2 = uasyncio.create_task(Regularly_hanle_msg(client,1))
    tasks.extend([t1, t2])
    await uasyncio.gather(*tasks)
    pass
    
if __name__ == '__main__':
#     pin40 = Pin(40,Pin.OUT)
#     while 1:
#         
#         led_on(pin40)
#         time.sleep(0.5)
#         led_off(pin40)
#         time.sleep(0.5)
    main()
    
    
    pass

#======================================================================================
#作者:trashedmaker
#开源文件,未注明请勿转载
#原文链接:https://blog.csdn.net/m0_73949172/article/details/144929662?spm=1001.2014.3001.5501
#======================================================================================    
    
    

