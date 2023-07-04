import time
from pulseapi import RobotPulse, pose, position, PulseApiException, SIG_HIGH, SIG_LOW, MT_LINEAR, output_action, \
    SystemState, create_box_obstacle, create_plane_obstacle, Point
from pdhttp.models import JointMotionParameters, LinearMotionParameters, InterpolationType, tool_info, tool_shape
from enum import Enum

host = "http://10.10.10.20:8081"  # Replace with a valid robot address
robot = RobotPulse(host)  # Create an instance of the API wrapper class

# Create motion poses
HOME_POSE = pose([0, -90, 0, -90, 0, 0])
START_POSE = pose([-170, -60, -137, -165, -84, 92])
FINISH_POSE = pose([-170, -58, -114, -190, -84.5, 92])

# Initial height above boxes
z = 0.25

TARGET_POSITIONS = [
    position([-0.3, 0.094, 0.28], [2.03, -1.49, 2.06]), # Moves straight ahead close to boxes[0]
    position([-0.3, 0.094, z], [2.03, -1.49, 2.06]), # Takes position to pick up the box[1]
    position([-0.3, 0.094, 0.60], [2.03, -1.49, 2.06]), # Moves straight up[2]
    position([0.118, 0.506, 0.6], [-0.026, -0.09, -1.558]), # Turns right non-linear[3]
    position([0.11, 0.4, 0.30], [0.016, 0.035, -1.536]), # Moves down to conveyor[4]
    position([-0.195, 0.4, 0.30], [0.016, 0.035, -1.536]), # Assemblies the box[5]
    position([-0.165, 0.4, 0.30], [0.016, 0.035, -1.536]), # Moves right for 3 centimeters[6]
    position([-0.165, 0.4, 0.25], [0.016, 0.035, -1.536]), # Moves down to place the box[7]
    position([-0.165, 0.35, 0.25], [0.016, 0.035, -1.536]), # Moves back for 5 centimeters[8]
    position([0.125, 0.52, 0.6], [-0.026, -0.09, -1.558]), # Takes a position to reach finish[9]
]

# Set the desired speed (controls both motor velocity and acceleration)
SPEED = 10
# Set the desired motor velocity(in centimeters per second?)
VELOCITY = 10
# Set the desired motor acceleration(in centimeters per second square?)
ACCELERATION = 5
# Radius of maximum deviation from the trajectory point (in metres)
BLEND=0.01

joint_motion_parameters = JointMotionParameters(
    velocity=VELOCITY,
    acceleration=ACCELERATION
)
linear_motion_parameters = LinearMotionParameters(
    # interpolation_type=InterpolationType.BLEND,
    velocity=VELOCITY,
    acceleration=ACCELERATION,
)

class TCP_VELOCITY(Enum):
    ONE_CM = 0.01,
    THREE_CM = 0.03,
    FIVE_CM = 0.05,
    TEN_CM = 0.1,
    FIFTEEN_CM = 0.15

def get_tcp_position():
    tcp_position = robot.get_position()
    while True:
        print("Current position: \n{}".format(tcp_position))
        time.sleep(5)


# Enter zero-gravity mode
robot.zg_on()

get_tcp_position()

# Disable zero-gravity mode
robot.zg_off()

# uncomment to make infinity cycle
# while True:
#     try:


# new_tool_shape = tool_shape(0.08, Point(0, 0, 0), Point(0.1, 0.2, 0.3), name="Jopa")
# robot.change_tool_shape(new_tool_shape)
# current_tool_info = robot.get_tool_info()
# current_tool_shape = robot.get_tool_shape()
# print("Current tool shape: \n{}".format(current_tool_shape))
# print("Current tool info: \n{}".format(current_tool_info))

# box = create_box_obstacle(
#     Point(-0.2, )
# )

def status_await_stop(robot_instance, asking_interval=0.1):
    await_status = robot_instance.status()
    while await_status == SystemState.MOTION:
        time.sleep(asking_interval)
        await_status = robot_instance.status()

i = 1

while i <= 1:  # The number of cycles
    try:
        i += 1
        z -= 0.01  # Arm Moves down for ... meters

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
        #                    tcp_max_velocity=TCP_VELOCITY.THREE_CM)
        # robot.set_position(position([-0.25, 0.1, 0.4], [2, -1.5, 2]),
        #                    tcp_max_velocity=TCP_VELOCITY.THREE_CM)


        robot.set_pose(HOME_POSE,
                       joint_motion_parameters)

        robot.set_pose(START_POSE,
                       joint_motion_parameters)  # Takes a starting position close to boxes

        robot.set_position(TARGET_POSITIONS[0],  # Moves straight ahead close to boxes
                           linear_motion_parameters)
        robot.set_position(position([-0.3, 0.094, z], [2.03, -1.49, 2.06]),  # Takes position and picks up the box
                           [output_action(1, SIG_HIGH)],
                           linear_motion_parameters)
        robot.set_position(TARGET_POSITIONS[2], # Moves straight up
                           joint_motion_parameters)
        robot.await_stop()

        robot.set_position(TARGET_POSITIONS[3],  # Turns right non-linear
                           joint_motion_parameters)
        robot.set_position(TARGET_POSITIONS[4],  # Moves down to conveyor
                           joint_motion_parameters)
        robot.set_position(TARGET_POSITIONS[5],  # Assemblies the box
                           joint_motion_parameters)
        robot.await_stop()

        robot.set_position(TARGET_POSITIONS[6],  # Moves right for 3 centimeters
                           joint_motion_parameters)
        # robot.await_stop()
        robot.set_position(TARGET_POSITIONS[7],  # Moves down to place the box
                           [output_action(1, SIG_LOW)],
                           joint_motion_parameters)
        robot.await_stop()
        robot.set_position(TARGET_POSITIONS[8],  # Moves back for 5 centimeters
                           joint_motion_parameters)
        robot.await_stop()

        robot.set_digital_output_high(2)  # Turns on the conveyor
        robot.await_stop(2)

        robot.set_position(TARGET_POSITIONS[9],  # Takes a position to reach finish
                           joint_motion_parameters)
        robot.await_stop()

        robot.set_digital_output_low(2)  # Turns off the conveyor

        robot.set_pose(FINISH_POSE,
                       joint_motion_parameters)
        robot.await_stop()

    except PulseApiException as e:
        # handle possible errors
        print("Exception {} while calling robot at {} ".format(e, robot.host))
        status = robot.status()
        failure = robot.status_failure()
        if status == SystemState.EMERGENCY:
            print("Robot is emergency. Error message: {}".format(failure))
        break