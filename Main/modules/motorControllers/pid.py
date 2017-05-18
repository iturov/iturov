#IMPORT LIBRARIES
#...

#CREATE CLASS
class PID(object):
    P = 0 # CREATE PROPORTIONAL VALUE
    I = 0 # CREATE INTEGRAL VALUE
    D = 0 # CREATE DERIVATIVE VALUE
    Eprev = 0 # CREATE PREVIOUS ERROR VALUE

    def __init__(self):
        # INITIALIZE OBJECT
        #...

    def calculate(self,setPoint,feedBack, Kp, Ki, Kd, dt):
        error = setPoint - feedBack
        P = error * Kp # CALCULATE P TERM
        I = I + error * Ki * dt # CALCULATE I TERM
        D = (error - Eprev) * Kd / dt # CALCULATE D TERM
        Eprev = error # UPDATE PREVIOUS ERROR BY NEW ERROR
        # NOTE: "dt" IS THE LOOP TIME
        return(P + I + D) # RETURN THE CALCULATED VALUE
