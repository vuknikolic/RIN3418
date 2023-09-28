import micropython, sys, gc, network, socket, esp, select, time, struct
from machine import Pin, I2C, PWM
from motor import motor

esp.osdebug(None)
gc.collect()

key = Pin(0,Pin.IN, Pin.PULL_UP)
led = Pin(15,Pin.OUT)

dcmotor = motor(3,5,7)
dcmotor2 = motor(2,4,6)

ssid = 'ESP32-S2'
pswd = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=pswd)
ap.ifconfig(('192.168.5.5', '255.255.255.0', '192.168.5.1','192.168.5.1'))

while ap.active() == False:
  pass

print(ap.ifconfig())

# ==========================================================

def listen_mcast():
    MCAST_GRP = '239.1.2.3'
    MCAST_PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.settimeout(3)
    s.bind(('', MCAST_PORT))
    s.setblocking(False)

    def inet_aton(ip):
        return bytes(map(int, ip.split(".")))

    INADDR_ANY = 0

    group = inet_aton(MCAST_GRP)
    mreq = struct.pack("4sL", group, INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return s

s = listen_mcast()

# ==========================================================
def byte_to_int(b):
    if b > 100:
        return b-256
    else:
        return b
    
while True:
    try:
        ready_socks, _, _ = select.select([s], [], [], 0)
        for ready_sock in ready_socks:
            data, addr = ready_sock.recvfrom(2)
            if len(data)==2:
                dcl = byte_to_int(data[0])
                dcr = byte_to_int(data[1])
                dcmotor.from_pid(int(dcl/3))
                dcmotor2.from_pid(int(dcr/3))
                print(dcl)
            else:
                s.close()
                s = listen_mcast()

            
    except OSError:
        pass    
        
    led.value(1)
    
    if key.value() == 0:
        led.value(0)
        sys.exit(0)
    
    led.value(0)

# ==========================================================   
