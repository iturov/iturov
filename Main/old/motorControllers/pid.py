#IMPORT LIBRARIES
#...

#CREATE CLASS
class PID(object):

    def __init__(self):
        self.P = 0 # CREATE PROPORTIONAL VALUE
        self.I = 0 # CREATE INTEGRAL VALUE
        self.D = 0 # CREATE DERIVATIVE VALUE
        self.Eprev = 0 # CREATE PREVIOUS ERROR VALUE

        # INITIALIZE OBJECT
        #...

    def calculate(self,setPoint,feedBack, Kp, Ki, Kd, dt):
        self.setPoint = setPoint
        self.feedBack = feedBack
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt

        self.error = self.setPoint - self.feedBack
        self.P = self.error * self.Kp # CALCULATE P TERM
        self.I = self.I + self.error * self.Ki * self.dt # CALCULATE I TERM
        self.D = (self.error - self.Eprev) * self.Kd / self.dt # CALCULATE D TERM
        self.Eprev = self.error # UPDATE PREVIOUS ERROR BY NEW ERROR
        # NOTE: "dt" IS THE LOOP TIME
        return(self.P + self.I + self.D) # RETURN THE CALCULATED VALUE
