import example_encoder
import time
import example_motor
import PID
import numpy as np
import math
import Lidar

if __name__ == "__main__":
    encoder = example_encoder.Encoder()
    encoder.start()
    motors = example_motor.Motor()

    PIDleft = PID.PID()
    PIDleft.Kd = 0
    PIDleft.Ki = .25
    PIDleft.Kp = .25

    PIDRight = PID.PID()
    PIDRight.Kd = 0
    PIDRight.Ki = .25
    PIDRight.Kp = .25

    lidar = Lidar.Lidar()


    def turn(angle):
        encoder.rightDistance = 0
        encoder.leftDistance = 0
        wheelBase = 21
        wheelRadius = 4
        print("rec dist : " + str((math.pi*(angle*(math.pi/180))* wheelBase)/(2* wheelRadius)))
        while (np.average([abs(encoder.leftDistance), abs(encoder.rightDistance)]) <
                   ((math.pi*(angle*(math.pi/180))* wheelBase)/(2* wheelRadius))):
            time.sleep(.05)
            measuredPhiDotLeft = -1*encoder.getPhiDotLeft()
            measuredPhiDotRight = encoder.getPhiDotRight()

            PIDleft.control(-.8, measuredPhiDotLeft, motors.setPhiDotDesiredLeft)
            PIDRight.control(.8, measuredPhiDotRight, motors.setPhiDotDesiredRight)

            # motors.PID(1,measuredPhiDotLeft,1.5,motors.setPhiDotDesiredLeft)
            # motors.PID(1,measuredPhiDotRight, 1.5, motors.setPhiDotDesiredRight)
            print("Phi Dot Right is: " + str(measuredPhiDotRight))
            print("Phi Dot Left is: " + str(measuredPhiDotLeft))

        print("left Dist " + str(encoder.leftDistance))
        print("right Dist " + str(encoder.rightDistance))


    def Forward(dist):
        encoder.rightDistance = 0
        encoder.leftDistance = 0
        while (np.average([abs(encoder.leftDistance), abs(encoder.rightDistance)]) < dist):
            time.sleep(.05)
            measuredPhiDotLeft = -1*encoder.getPhiDotLeft()
            measuredPhiDotRight = encoder.getPhiDotRight()

            PIDleft.control(1.5, measuredPhiDotLeft, motors.setPhiDotDesiredLeft)
            PIDRight.control(1.5, measuredPhiDotRight, motors.setPhiDotDesiredRight)

            motors.PID(1,measuredPhiDotLeft,1.5,motors.setPhiDotDesiredLeft)
            motors.PID(1,measuredPhiDotRight, 1.5, motors.setPhiDotDesiredRight)
            #print("Phi Dot Right is: " + str(measuredPhiDotRight))
            #print("Phi Dot Left is: " + str(measuredPhiDotLeft))

        print("left Dist " + str(encoder.leftDistance))
        print("rightt Dist " + str(encoder.rightDistance))

    lidar.ml = motors
    lidar.start()
    Forward(1000)
    # turn(95)
    # Forward(100)
    # turn(95)
    # Forward(100)
    # turn(95)
    # Forward(100)
    # turn(95)
    # for x in range(50):
    #     time.sleep(.05)
    #     measuredPhiDotLeft = encoder.getPhiDotLeft()
    #     measuredPhiDotRight = encoder.getPhiDotRight()
    #
    #     PIDleft.control(2,measuredPhiDotLeft,motors.setPhiDotDesiredLeft)
    #     PIDRight.control(2,measuredPhiDotRight,motors.setPhiDotDesiredRight)
    #
    #     #motors.PID(1,measuredPhiDotLeft,1.5,motors.setPhiDotDesiredLeft)
    #     #motors.PID(1,measuredPhiDotRight, 1.5, motors.setPhiDotDesiredRight)
    #
    #     print("Phi Dot Right is: "+str(measuredPhiDotRight))
    #     print("Phi Dot Left is: " + str(measuredPhiDotLeft))



    motors.brake()
    motors.off()

