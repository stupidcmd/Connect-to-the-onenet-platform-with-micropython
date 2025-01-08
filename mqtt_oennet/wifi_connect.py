import network
import time

class wifi():
    def __init__(self,ssid,password):
        self.ssid=ssid
        self.password=password
        self.wlan_connect()
    def wlan_connect(self):
        #1创建局域网对象使用STA_IF站点模式（AP_IF为服务端模式）
        wlan = network.WLAN(network.STA_IF)
        #2激活网络
        wlan.active(1)
        #3扫描网络
        wlan.scan()
        #4连接网络并等待成功
        if not wlan.isconnected():
            wlan.connect(self.ssid,self.password)
            print("wifi is connecting...")
            i=1
            while not wlan.isconnected():
                print("try time:%d"%i)
                i+=1
                time.sleep(1)
        #5打印连接属性
        print("network:",wlan.ifconfig())
        print("ssid:",wlan.config("essid"))
        print("mac:",wlan.config("mac"))
        
if __name__ == '__main__':

    wlan = wifi(ssid = "CMCC-9mZu",password = "hhh2j9jw")
    wlan.wlan_connect()