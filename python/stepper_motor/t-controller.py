import random

F_MAX = 2000
F_MIN = 100


class Pulse(object):
    def __init__(self, id, freq, tstart=0):
        self.id = id
        self.freq = freq
        self.period = 1 / self.freq 
        self.tstart = tstart 
        self.tend = self.tstart + self.period

    def __str__(self):
        return 'pulse-{:04}, {:2.6f} Hz, {:2.6f} ms, time: {:2.6f} -> {:2.6f}'.format(
                self.id, 
                self.freq, 
                self.period * 1000, 
                self.tstart, 
                self.tend)


def predict(fmax, P):
    pulses = [Pulse(1, F_MIN)]

    for id in range(2, P+1):
        
        lp = pulses[-1]
        id = lp.id + 1

        if lp.id < 200:
            df = (fmax - lp.freq) / (200 - lp.id)
            f = lp.freq + df
        else:
            f = fmax

        p = Pulse(id, f, tstart=lp.tend)
        pulses.append(p)
        
    #[print(p) for p in pulses]

    lp = pulses[-1]
    return lp.tend


def find_fmax(T, P):
    fmax = F_MAX 
    fmin = F_MIN 
    f = random.choice(range(fmin, fmax))
    #f = (fmax + fmin) // 2
    count = 0

    while True:
        count += 1
        print('----------------- round {}'.format(count))
        if count > 20:
            return f 

        tp = predict(f, P)
        print('predict({}) = {} compare with {}'.format(f, tp, T))

        if tp > T:
            fmin = f
            print('select freq from {} ~ {}'.format(f, fmax))
            freqs = range(f, fmax)
            f = random.choice(freqs)
        elif tp < T:
            fmax = f
            print('select freq from {} ~ {}'.format(f, fmin))
            freqs = range(fmin, f)
            f = random.choice(freqs)

        if (fmax - fmin) == 1:
            return f
            
    
class StepperMotorPulseGenerator(object):
    def __init__(self, T, P):
        self.target_time = T
        self.total_pulses = P


    def find_fmax(self):
        fmax = find_fmax(self.target_time, self.total_pulses)
        return fmax


    def predict(self, f, P):
        return predict(f, P)


def main(opts):
    T = opts.target_time
    P = opts.total_pulses

    g = StepperMotorPulseGenerator(T, P)
    fmax = g.find_fmax()

    print('--------------------------')
    print('find fmax: {}'.format(fmax))


    tp = g.predict(fmax, P)
    print('predict({}, {}) = {}'.format(fmax, P, tp))

    f = fmax + 1
    tp = g.predict(f, P)
    print('predict({}, {}) = {}'.format(f, P, tp))


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()

    parser.add_option('-T', 
                      dest='target_time',
                      type="int", 
                      default=4,
                      help='Target time(second) for motor move to target location[default=%default]')
    parser.add_option('-P', 
                      dest='total_pulses',
                      type="int", 
                      default=1000,
                      help='Total steps(pulses) for motor move to target location[default=%default]')

    opts, args = parser.parse_args()
    print(opts)
    print(args)
    main(opts)


