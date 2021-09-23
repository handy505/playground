import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


from pid import PIDController


'''con = PIDController(4, 4, 1.5)


# animate plots?
animate=True# True / False

# define model
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

#tf = 60.0                 # final time for simulation
tf = 160.0                 # final time for simulation
nsteps = 61               # number of time steps
#nsteps = 161               # number of time steps
delta_t = tf/(nsteps-1)   # how long is each time step?
ts = np.linspace(0,tf,nsteps) # linearly spaced time vector

# simulate step test operation
step = np.zeros(nsteps) # u = valve % open
step[11:] = 50.0       # step up pedal position
# passenger(s) + cargo load
load = 200.0 # kg
# velocity initial condition
v0 = 0.0
# set point
sp = 25.0
# for storing the results
vs = np.zeros(nsteps)
sps = np.zeros(nsteps)

plt.figure(1,figsize=(5,4))
if animate:
    plt.ion()
    plt.show()


# simulate with ODEINT
for i in range(nsteps-1):
    prev_v = vs[i]
    prev_sp = sps[i]
    error = prev_sp - prev_v
    u = con.update(error)
    #u = step[i]
    # clip inputs to -50% to 100%
    if u >= 100.0:
        u = 100.0
    if u <= -50.0:
        u = -50.0
    step[i] = u

    v = odeint(vehicle,v0,[0,delta_t],args=(u,load))
    print(v)
    v0 = v[-1]   # take the last value
    vs[i+1] = v0 # store the velocity for plotting
    sps[i+1] = sp

    # plot results
    if animate:
        plt.clf()
        plt.subplot(2,1,1)
        plt.plot(ts[0:i+1],vs[0:i+1],'b-',linewidth=3)
        plt.plot(ts[0:i+1],sps[0:i+1],'k--',linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity','Set Point'],loc=2)
        plt.subplot(2,1,2)
        plt.plot(ts[0:i+1],step[0:i+1],'r--',linewidth=3)
        plt.ylabel('Gas Pedal')    
        plt.legend(['Gas Pedal (%)'])
        plt.xlabel('Time (sec)')
        #plt.pause(0.1)    
        plt.pause(0.5)    
        #input()
        '''


'''if not animate:
    # plot results
    plt.subplot(2,1,1)
    plt.plot(ts,vs,'b-',linewidth=3)
    plt.plot(ts,sps,'k--',linewidth=2)
    plt.ylabel('Velocity (m/s)')
    plt.legend(['Velocity','Set Point'],loc=2)

    plt.subplot(2,1,2)
    plt.plot(ts,step,'r--',linewidth=3)
    plt.ylabel('Gas Pedal')    
    plt.legend(['Gas Pedal (%)'])
    plt.xlabel('Time (sec)')
    

    plt.show()
    '''



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
        plt.figure(1,figsize=(5,4))
        plt.ion()
        plt.show()


    def run(self):
        tf = 60.0                       # final time for simulation
        nsteps = 61                     # number of time steps
        delta_t = tf/(nsteps-1)         # how long is each time step?

        self.ts = np.linspace(0, tf, nsteps) # linearly spaced time vector

        # simulate step test operation
        self.step = np.zeros(nsteps) # u = valve % open
        self.vs   = np.zeros(nsteps)
        self.sps  = np.zeros(nsteps)



        car = Car(200.0)
        con = PIDController(4, 4, 1.5)

        target = 25
        v = 0
        u = 0

        for i in range(nsteps-1):

            e = target - v

            u = con.update(e)
            if u >= 100.0:
                u = 100.0
            if u <= -50.0:
                u = -50.0

            self.step[i] = u

            v = car.update(u, delta_t)
            print(v)

            self.vs[i+1] = v # store the velocity for plotting
            self.sps[i+1] = target 


            self.draw(i)




    def draw(self, i):
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




def main():
    animate = True
    plt.figure(1,figsize=(5,4))
    if animate:
        plt.ion()
        plt.show()


    tf = 60.0                      # final time for simulation
    nsteps = 61                     # number of time steps
    delta_t = tf/(nsteps-1)         # how long is each time step?

    ts = np.linspace(0, tf, nsteps) # linearly spaced time vector

    # simulate step test operation
    step = np.zeros(nsteps) # u = valve % open
    vs   = np.zeros(nsteps)
    sps  = np.zeros(nsteps)




    car = Car(200.0)
    con = PIDController(4, 4, 1.5)

    target = 25
    v = 0
    u = 0

    for i in range(nsteps-1):

        e = target - v

        u = con.update(e)
        if u >= 100.0:
            u = 100.0
        if u <= -50.0:
            u = -50.0

        step[i] = u

        v = car.update(u, delta_t)
        print(v)

        vs[i+1] = v # store the velocity for plotting
        sps[i+1] = target 


        plt.clf()
        plt.subplot(2,1,1)
        plt.plot(ts[0:i+1],vs[0:i+1],'b-',linewidth=3)
        plt.plot(ts[0:i+1],sps[0:i+1],'k--',linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity','Set Point'],loc=2)
        plt.subplot(2,1,2)
        plt.plot(ts[0:i+1],step[0:i+1],'r--',linewidth=3)
        plt.ylabel('Gas Pedal')    
        plt.legend(['Gas Pedal (%)'])
        plt.xlabel('Time (sec)')
        plt.pause(0.1)    
        #input()



if __name__ == '__main__':
    #main()
    s = Simulator()
    s.run()
