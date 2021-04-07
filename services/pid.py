import numpy as np

def limit_angle(angle, max_angle):
    # limitiert den Winkel auf einen +/-halben Kreis, z.B. auf max. -180°..180°
    half = max_angle / 2
    return (angle + half) % max_angle - half


class PID_angle(object):
    type = 'pid_angle'

    def __init__(self, name, p=0, i=0, d=0, time=0, angle_max=float('inf'), out_min=float('inf'), out_max=float('inf'),
                 anti_windup=1, target=0):
        self.name = name
        self.tune(p, i, d)
        self.target = target
        self._prev_time = time
        self._prev_error = 0
        self.error = None
        self.angle_max = angle_max
        self.integral = 0
        self.out_min = out_min
        self.out_max = out_max
        self.anti_windup = anti_windup

    def __call__(self, feedback, target=None, time=None):
        if target is not None: self.target = target
        error = self.error = limit_angle(self.target - feedback, self.angle_max)
        if time is None:
            dt = 1
        else:
            dt = time - self._prev_time
        err_diff = limit_angle(error - self._prev_error, self.angle_max)
        if np.sign(error) != np.sign(self._prev_error):
            self.integral = self.integral / self.anti_windup
        self.integral += error * dt
        self.derivative = 0
        if dt != 0:
            self.derivative = (err_diff) / dt
        self._prev_error = error
        out = self._p * error + self._i * self.integral + self._d * self.derivative
        out = np.clip(out, self.out_min, self.out_max)
        self._prev_time = time
        # print('PID {}: {}->{} (t={})'.format(self.name, feedback, out, self.target))
        return out

    def tune(self, p, i, d):
        self._p = p
        self._i = i
        self._d = d
        self._prev_error = 0
        self.integral = 0