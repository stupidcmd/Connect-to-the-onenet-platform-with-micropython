from machine import Pin



def led_on(gpio):
    gpio.value(1)
    pass
def led_off(gpio):
    gpio.value(0)
    pass




if __name__ == '__main__':
    
    led40 = Pin(40, Pin.OUT)
    led40.value(0)
    
    pass