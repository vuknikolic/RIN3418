import machine
import time

class mpu():

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    PI = 3.14159265358979323846
    radToDeg = 180.0 / PI

    ADDRESS = 0x68
    
    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0
 
    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4
 
    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18
 
    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18
 
    # MPU6050 registri
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C
      
    # raw data 14 bajtova nema potrebe da se uzima pojedinacno iz svakog registra
    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40
    TEMP_OUT0 = 0x41
    TEMP_OUT1 = 0x42
    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48
 
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C

    def __init__(self, i2c, addr=ADDRESS):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([self.PWR_MGMT_1, 0x00]))
        self.iic.writeto(self.addr, bytearray([self.ACCEL_CONFIG, self.ACCEL_RANGE_2G]))
        self.iic.writeto(self.addr, bytearray([self.GYRO_CONFIG, self.GYRO_RANGE_250DEG]))
        self.iic.writeto(self.addr, bytearray([self.CONFIG, 0x00]))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, self.ACCEL_XOUT0, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values_tuple(self):
        raw_ints = self.get_raw_values()
        vals = [
            time.ticks_us() / 1000000,
            self.bytes_toint(raw_ints[0], raw_ints[1])/16384 * self.GRAVITIY_MS2,
            self.bytes_toint(raw_ints[2], raw_ints[3])/16384 * self.GRAVITIY_MS2,
            self.bytes_toint(raw_ints[4], raw_ints[5])/16384 * self.GRAVITIY_MS2,
            self.bytes_toint(raw_ints[8], raw_ints[9])/131 / self.radToDeg,
            self.bytes_toint(raw_ints[10], raw_ints[11])/131 / self.radToDeg,
            self.bytes_toint(raw_ints[12], raw_ints[13])/131 / self.radToDeg,
            ]
        return vals

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1]) 
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3]) 
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5]) 
        #vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9]) 
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11]) 
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        vals["time"] = str(time.ticks_us())
        return vals  # returned in range of Int16
