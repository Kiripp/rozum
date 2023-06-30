from pulseapi import RobotPulse, pose, position, PulseApiException, SIG_HIGH, SIG_LOW, MT_LINEAR, output_action

host = "http://10.10.10.20:8081"  # replace with a valid robot address
robot = RobotPulse(host)  # create an instance of the API wrapper class

# create motion targets
home_pose = pose([0, -90, 0, -90, 0, 0])
start_pose = pose([-170, -60, -137, -165, -84, 92])
finish_pose = pose([-170, -58, -114, -190, -84.5, 92])
# initial height above boxes
z = 0.25
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

        # i = 1

        # while i <= 1:  # The number of cycles
        #     try:
        #         i += 1
        #         z -= 0.01  # Arm goes down for ... meters

        # recover_result = robot.recover() # Recovery if arm's led signal is red
        # print("Recover result: {}".format(recover_result))

        # Makes arm go up & down
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    acceleration=ACCELERATION,
        #                    velocity=VELOCITY)
        # robot.set_position(position([-0.25, 0.1, 0.4], [2, -1.5, 2]),
        #                    acceleration=ACCELERATION,
        #                    velocity=VELOCITY)
        # robot.set_position(position([-0.25, 0.1, 0.3], [2, -1.5, 2]),
        #                    tcp_max_velocity=TCP_VELOCITY_3CM)
        # robot.set_position(position([-0.25, 0.1, 0.4], [2, -1.5, 2]),
        #                    tcp_max_velocity=TCP_VELOCITY_3CM)
        #

        # robot.set_pose(home_pose,
        #                velocity=VELOCITY,
        #                acceleration=ACCELERATION)

        robot.set_pose(start_pose,
                       velocity=VELOCITY,
                       acceleration=ACCELERATION)  # Takes a starting position close to boxes

        robot.set_position(position([-0.3, 0.094, 0.28], [2.03, -1.49, 2.06]),  # Goes straight ahead close to boxes
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,
                           motion_type=MT_LINEAR)

        robot.set_position(position([-0.3, 0.094, z], [2.03, -1.49, 2.06]),
                           [output_action(1, SIG_HIGH)],
                           acceleration=ACCELERATION,
                           velocity=VELOCITY,
                           motion_type=MT_LINEAR)
        robot.set_position(position([-0.3, 0.094, 0.60], [2.03, -1.49, 2.06]),
                           acceleration=ACCELERATION,
                           velocity=VELOCITY)
        robot.await_stop()
        robot.set_position(position([0.118, 0.506, 0.6], [-0.026, -0.09, -1.558]),  # Turns right non-linear
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.set_position(position([0.11, 0.4, 0.30], [0.016, 0.035, -1.536]),  # Goes down to conveyor
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.set_position(position([-0.195, 0.4, 0.30], [0.016, 0.035, -1.536]),  # Box assembly
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.await_stop()
        robot.set_position(position([-0.165, 0.4, 0.30], [0.016, 0.035, -1.536]),  # Goes right for 3 cm
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.await_stop()
        robot.set_position(position([-0.165, 0.4, 0.25], [0.016, 0.035, -1.536]),  # Goes down to place the box
                           [output_action(1, SIG_LOW)],
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.await_stop()

        robot.set_position(position([-0.165, 0.35, 0.25], [0.016, 0.035, -1.536]),  # Goes back for 5 cm
                           acceleration=ACCELERATION,
                           velocity=VELOCITY)
        robot.await_stop()

        robot.set_digital_output_high(2)  # Turns on the conveyor
        robot.await_stop(2)

        robot.set_position(position([0.125, 0.52, 0.6], [-0.026, -0.09, -1.558]),  # Takes a position to back home
                           acceleration=ACCELERATION,
                           velocity=VELOCITY, )
        robot.await_stop(1)

        robot.set_digital_output_low(2)  # Turns off the conveyor

        robot.set_pose(finish_pose,
                       velocity=VELOCITY,
                       acceleration=ACCELERATION)
        robot.await_stop(1)

    except PulseApiException as e:
        # handle possible errors
        print("Exception {} while calling robot at {} ".format(e, robot.host))
        break
