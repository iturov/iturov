# storing Integral, and the previous error to calculate rate of change in the error
I = 0
error_prev = 0

def calculate(setpoint, feedback, kp, ki, kd, dt):
    error = setpoint - feedback
    P = error * kp
    I += error * ki * dt
    D = (error - error_prev) * kd / dt
    error_prev = error
    # NOTE: DT IS LOOP TIME
    return (P + I + D)
