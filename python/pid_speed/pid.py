import time

class PIDController(object):
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd 

        #self.pvalue = 0.0
        self.ivalue = 0.0
        #self.dvalue = 0.0

        self.prev_time = time.time()
        self.prev_error = 0.0


    def update(self, error, current_time=None):
        if current_time is None:
            current_time = time.time()

        dt = current_time - self.prev_time

        de = error - self.prev_error

        print('de: {}, dt: {}'.format(de, dt))

        pvalue = error
        pterm = self.Kp * pvalue


        self.ivalue += error * dt
        iterm = self.Ki * self.ivalue 




        dvalue = de / dt
        dterm = self.Kd * dvalue

        #print('p: {}, i: {}, d: {}'.format(self.pvalue, self.ivalue, self.dvalue))
        print('p: {}, i: {}, d: {}'.format(pterm, iterm, dterm))

        self.prev_time = current_time
        self.prev_error = error

        #result = (self.Kp * self.pvalue) + (self.Ki * self.ivalue) + (self.Kd * self.dvalue)
        result = pterm + iterm + dterm
        return result



if __name__ == '__main__':
    c = PIDController(1.2, 0.8, 0.1)

    target = 100

    time.sleep(0.1)

    for _ in range(0, 10):

        error = target - 80
        r = c.update(error)
        print(r)
        print('----')

        time.sleep(0.1)






