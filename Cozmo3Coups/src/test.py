#!/usr/bin/python3


import cozmo

import chifoumi
import robotchifoumi
from robotchifoumi import RobotChifoumi


def testGameEnd(r: cozmo.robot.Robot):
    robot = RobotChifoumi(r)

    robot.react_to_game_end(5, 3)
    robot.react_to_game_end(0, 3)
    robot.react_to_game_end(1, 3)
    robot.react_to_game_end(2, 3)
    robot.react_to_game_end(3, 0)
    robot.react_to_game_end(3, 2)


def testConnectToLightCubes(robot):
    robot.world.connect_to_cubes()
    robot.world.auto_disconnect_from_cubes_at_end()

    for c in robot.world.connected_light_cubes:
        print(c)


def testImages(robot: cozmo.robot.Robot):
    robot_cozmo = robotchifoumi.RobotChifoumi(robot)

    #for image in robot_cozmo.images:
     #   robot_cozmo.robot.display_oled_face_image(image.value, 200).wait_for_completed()

    robot_cozmo.robot.display_oled_face_image(robot_cozmo.images[chifoumi.Coup.ROCK], 5000).wait_for_completed()
    robot_cozmo.robot.display_oled_face_image(robot_cozmo.images[chifoumi.Coup.PAPER], 5000).wait_for_completed()
    robot_cozmo.robot.display_oled_face_image(robot_cozmo.images[chifoumi.Coup.SCISSORS], 5000).wait_for_completed()


cozmo.run_program(testGameEnd)
