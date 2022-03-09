import time

import cozmo

def hand_track(robot: cozmo.robot.Robot):
    robot.move_head(1.0)
    robot.world.visible_face_count()
    time.sleep(100)


cozmo.run_program(hand_track, use_viewer=True)