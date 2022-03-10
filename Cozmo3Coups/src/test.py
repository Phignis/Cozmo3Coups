#!/usr/bin/python3


import cozmo
from robotchifoumi import RobotChifoumi


def testGameEnd(r: cozmo.robot.Robot):
    robot = RobotChifoumi(r)

    robot.react_to_game_end(0, 3)
    robot.react_to_game_end(1, 3)
    robot.react_to_game_end(2, 3)
    robot.react_to_game_end(3, 0)
    robot.react_to_game_end(3, 1)
    robot.react_to_game_end(3, 2)


def testConnectToLightCubes(robot):
    robot.world.connect_to_cubes()
    robot.world.auto_disconnect_from_cubes_at_end()

    for c in robot.world.connected_light_cubes:
        print(c)


cozmo.run_program(testConnectToLightCubes)
