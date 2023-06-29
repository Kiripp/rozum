# import math
from pulseapi import RobotPulse, pose, position, PulseApiException, SIG_HIGH, SIG_LOW, MT_LINEAR, output_action

host = "http://10.10.10.20:8081"  # replace with a valid robot address
robot = RobotPulse(host)  # create an instance of the API wrapper class

# create motion targets
home_pose = pose([0, -90, 0, -90, 0, 0])
start_pose = pose([-170, -60, -137, -165, -84, 92])
finish_pose = pose([-170, -58, -114, -190, -84.5, 92])
# initial height above boxes
z = 0.23
float(z)

# set the desired speed (controls both motor velocity and acceleration)
SPEED = 7.5
# set the desired motor velocity
VELOCITY = 10
# set the desired motor acceleration
ACCELERATION = 6

# set the desired tcp velocity
TCP_VELOCITY_1CM = 0.01
TCP_VELOCITY_2CM = 0.02
TCP_VELOCITY_3CM = 0.03
TCP_VELOCITY_5CM = 0.05
TCP_VELOCITY_8CM = 0.08
TCP_VELOCITY_10CM = 0.1
TCP_VELOCITY_15CM = 0.15
TCP_VELOCITY_20CM = 0.2
TCP_VELOCITY_25CM = 0.25

# uncomment to make infinity cycle
while True:
    try:

# i = 1  ### iterator
# #
# while i <= 1:  # the number of cycles
#     try:
#         i += 1
#         z -= 0.01  ### arm goes down for ... meters


        ### RECOVERY IF ARM'S LED SIGNAL IS RED
        # recover_result = robot.recover()
        # print("Recover result: {}".format(recover_result))
        ###

        # UP AND DOWN
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    acceleration=ACCELERATION,
        #                    velocity=VELOCITY)
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    acceleration=ACCELERATION,
        #                    velocity=VELOCITY)
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    tcp_max_velocity=TCP_VELOCITY_3CM)
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    tcp_max_velocity=TCP_VELOCITY_3CM)
        # robot.await_stop(0.5)

        # print("Current pose: \n{}".format(robot.get_pose())) ### gets arm's pose info (degrees for all axis)
        # print("Current position: \n{}".format(robot.get_position())) ### gets arm's position info (x, y, z)
        # print("Status motors: \n{}".format(robot.status_motors())) ### gets arm's motors' info
        # print("Status:  \n{}".format(robot.state())) ### gets arm's status info

        ### ARM'S STATE BLOCK
        robot.freeze()  ### switches arm's state to FREEZE state (stays still)
        # robot.relax() ### switches arm's state to RELAX state (moves freely)
        ###

        # robot.set_pose(home_pose, SPEED) ### 0, -90, 0, -90, 0, 0
        # robot.set_pose(start_pose, SPEED)  ### takes a starting position close to boxes

        robot.set_pose(start_pose, velocity=VELOCITY, acceleration=ACCELERATION)  ### takes a starting position close to boxes

        robot.set_position(position([-0.3, 0.094, 0.28], [2.03, -1.49, 2.06]), ### goes straight ahead close to boxes
                            acceleration=ACCELERATION,
                           velocity=VELOCITY,
                           motion_type=MT_LINEAR,) ### sets linear motion type
        robot.set_position(position([-0.3, 0.094, z], [2.03, -1.49, 2.06], [output_action(1, SIG_HIGH)]),
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,
                           motion_type=MT_LINEAR) ### sets linear motion type
        robot.set_position(position([-0.3, 0.094, 0.60], [2.03, -1.49, 2.06]), ### GOES UP WITH BOX
                           acceleration=ACCELERATION,
                           velocity=VELOCITY)
        robot.await_stop(0.5)
        robot.set_position(position([0.118, 0.506, 0.6], [-0.026, -0.09, -1.558]), ### TURNS RIGHT NON-LINEAR
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,)
        robot.set_position(position([0.11, 0.4, 0.30], [0.016, 0.035, -1.536]),  ### опускается к конвейеру
                            acceleration=ACCELERATION,
                           velocity=VELOCITY,)
                           # motion_type=MT_LINEAR)  ### sets linear motion type
        robot.set_position(position([-0.195, 0.4, 0.30], [0.016, 0.035, -1.536]),  ### box assembly
                            acceleration=ACCELERATION,
                           velocity=VELOCITY,)
                           # motion_type=MT_LINEAR)  ### sets linear motion type
        robot.await_stop()
        robot.set_position(position([-0.165, 0.4, 0.30], [0.016, 0.035, -1.536]),  ### goes right for 3 cm
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,)
                           # motion_type=MT_LINEAR)
        robot.await_stop()
        robot.set_position(position([-0.165, 0.4, 0.25], [0.016, 0.035, -1.536],  ### goes down to place the box
                                    [output_action(1, SIG_LOW)]),
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,)
                           # motion_type=MT_LINEAR) ### sets linear motion type
        robot.await_stop()
        robot.set_position(position([-0.165, 0.35, 0.25], [0.016, 0.035, -1.536]),  ### moves back for 5 cm as not to
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,)  ### touch the box
        #                   # motion_type=MT_LINEAR) ### sets linear motion type
        robot.await_stop()
        robot.set_digital_output_high(2)  ### turns on the conveyor

        robot.await_stop(2)

        ## robot.await_stop(2)  ### waits for 2 seconds before turning off the conveyor

        robot.set_position(position([0.125, 0.52, 0.6], [-0.026, -0.09, -1.558]), ### POSITION TO BACK HOME SAFELY
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,)
        robot.await_stop(1)

        robot.set_digital_output_low(2) ### turns off the conveyor

        robot.set_pose(finish_pose, velocity=VELOCITY, acceleration=ACCELERATION) ### BACKS HOME
        robot.await_stop(1)

    except PulseApiException as e:
        # handle possible errors
        print("Exception {} while calling robot at {} ".format(e, robot.host))
        break
