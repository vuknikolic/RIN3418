from machine import Pin, PWM
import math

class motor:      
  def __init__(self, pwm_pin, in1_pin, in2_pin):
    self.pwm0 = PWM(Pin(pwm_pin), freq=1000, duty_u16=0)
    self.in1 = Pin(in1_pin,Pin.OUT)
    self.in2 = Pin(in2_pin,Pin.OUT)

  def napred(self,speed):
    self.in1.value(1)
    self.in2.value(0)
    self.pwm0.duty_u16(speed)    

  def nazad(self, speed):
    self.in1.value(0)
    self.in2.value(1)
    self.pwm0.duty_u16(speed)    
  
  def stop(self):
    self.pwm0.duty_u16(0)    
    self.in1.value(1)
    self.in2.value(1)

  def from_pid(self,pid_output):
    if pid_output>0:
        self.in1.value(1)
        self.in2.value(0)
        if pid_output>20:
            self.pwm0.duty_u16(65535)    
        else:
            self.pwm0.duty_u16(int(pid_output*3200))    
    else:
        self.in1.value(0)
        self.in2.value(1)
        if pid_output<-20:
            self.pwm0.duty_u16(65535)    
        else:
            self.pwm0.duty_u16(int(pid_output*(-3200)))    
     
 

