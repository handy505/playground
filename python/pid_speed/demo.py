import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

from pid import PIDController

import sys



def vehicle(v,t,u,load):
    # inputs
    #  v    = vehicle velocity (m/s)
    #  t    = time (sec)
    #  u    = gas pedal position (-50% to 100%)
    #  load = passenger load + cargo (kg)
    Cd = 0.24    # drag coefficient
    rho = 1.225  # air density (kg/m^3)
    A = 5.0      # cross-sectional area (m^2)
    Fp = 30      # thrust parameter (N/%pedal)
    m = 500      # vehicle mass (kg)
    # calculate derivative of the velocity
    dv_dt = (1.0/(m+load)) * (Fp*u - 0.5*rho*Cd*A*v**2)
    return dv_dt


class Car(object):
    def __init__(self, load):
        self.load = load
        self.v = 0.0

    def update(self, u, delta_t):
        #v = odeint(vehicle, v0, [0, delta_t], args=(u, self.load))
        vs = odeint(vehicle, self.v, [0, delta_t], args=(u, self.load))
        #v0 = v[-1]   # take the last value
        self.v = vs[-1]
        return self.v


class Simulator(object):
    def __init__(self):
        plt.figure(1,figsize=(8,6))

        #self.animate = True 
        self.animate = False 
        if self.animate:
            plt.ion()
            plt.show()



        self.car = Car(200.0)

        self.Kp = 16
        self.Ki = 0.2
        self.Kd = 0.8 
        self.con = PIDController(self.Kp, self.Ki, self.Kd)
        self.con.prev_time = -1



    def limit(self, u):
        if u >= 100.0:
            u = 100.0
        if u <= -50.0:
            u = -50.0
        return u


    def run(self):
        tf = 60.0                       # final time for simulation
        nsteps = 61                     # number of time steps
        delta_t = tf/(nsteps-1)         # how long is each time step?

        self.ts = np.linspace(0, tf, nsteps) # linearly spaced time vector

        # simulate step test operation
        self.step = np.zeros(nsteps) # u = valve % open
        self.vs   = np.zeros(nsteps)
        self.sps  = np.zeros(nsteps)


        target = 25
        v = 0
        u = 0

        for i in range(nsteps-1):

            e = target - v

            u = self.con.update(e, current_time=self.ts[i])
            u = self.limit(u)

            self.step[i] = u

            v = self.car.update(u, delta_t)
            print('v: {}'.format(v))

            self.vs[i+1] = v # store the velocity for plotting
            self.sps[i+1] = target 


            if self.animate:
                self.draw_animate(i)

        if not self.animate:
            self.draw_picture()
        else:
            input()

    def draw_animate(self, i):
        plt.clf()

        plt.subplot(2,1,1)
        plt.plot(self.ts[0:i+1], self.vs[0:i+1], 'b-', linewidth=3)
        plt.plot(self.ts[0:i+1], self.sps[0:i+1], 'k--', linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity','Set Point'],loc=2)

        plt.subplot(2,1,2)
        plt.plot(self.ts[0:i+1], self.step[0:i+1], 'r--', linewidth=3)
        plt.ylabel('Gas Pedal')    
        plt.legend(['Gas Pedal (%)'])

        plt.xlabel('Time (sec)')
        plt.pause(0.1)    
        #input()


    def draw_picture(self):
        # plot results
        plt.subplot(2,1,1)
        plt.plot(self.ts, self.vs, 'b-', linewidth=3)
        plt.plot(self.ts, self.sps, 'k--', linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity','Set Point'],loc=2)

        plt.subplot(2,1,2)
        plt.plot(self.ts, self.step, 'r--', linewidth=3)
        plt.ylabel('Gas Pedal')    
        plt.legend(['Gas Pedal (%)'])
        plt.xlabel('Time (sec)')
        
        s = 'Kp:{}, Ki:{}, Kd:{}'.format(self.Kp, self.Ki, self.Kd)
        plt.text(0, 0, s, fontsize=15)

        plt.show()


if __name__ == '__main__':
    s = Simulator()
    s.run()
