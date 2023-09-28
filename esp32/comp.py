import math

class imu:



    def __init__(self):

        self.GRAVITIY_MS2 = 9.80665
        self.PI = 3.14159265358979323846
        self.radToDeg = 180.0 / self.PI
        
        self.cutoff = 1.0
        self.RC = 1.0 / (2.0 * self.PI * self.cutoff)

        self.alpha = 0.01

        self.prev_sample_time = 0
        self.ax_f = 0
        self.ay_f = 0
        self.az_f = 0
        self.phi_g_dot = 0
        self.theta_g_dot = 0
        self.phi_comp = 0
        self.theta_comp = 0

    def render(self,sample):
        dt = sample[0]-self.prev_sample_time
        self.prev_sample_time = sample[0] 
        if dt > 0:
            LPF = dt / (self.RC + dt)
            HPF = self.RC / (self.RC + dt)
            self.ax_f = LPF * sample[1] + (1-LPF) * self.ax_f
            self.ay_f = LPF * sample[2] + (1-LPF) * self.ay_f
            self.az_f = LPF * sample[3] + (1-LPF) * self.az_f

            phi_a = math.atan2(self.ay_f, math.sqrt(self.ax_f ** 2.0 + self.az_f ** 2.0))
            theta_a = math.atan2(-self.ax_f, math.sqrt(self.ay_f ** 2.0 + self.az_f ** 2.0))
        
            phi_g = self.phi_g_dot + sample[4]*dt
            theta_g = self.theta_g_dot + sample[5]*dt
            self.phi_g_dot = phi_g
            self.theta_g_dot = theta_g   
        
            self.phi_comp = self.alpha * phi_a + (1-self.alpha) * (self.phi_comp + dt * sample[4])
            self.theta_comp = self.alpha * theta_a + (1-self.alpha) * (self.theta_comp +  dt * sample[5])
        return self.phi_comp*self.radToDeg,self.theta_comp*self.radToDeg
