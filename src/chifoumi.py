#!/usr/bin/python3

import cozmo
import time
import asyncio



def chifoumi(robot: cozmo.robot.Robot):
	robot.enable_stop_on_cliff(False)
	robot.drive_off_charger_contacts().wait_for_completed()

	robot.set_lift_height(1).wait_for_completed()


	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
	try:
		tetePersonne = robot.world.wait_for_observed_face(timeout=10)
	except:
		robot.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
	finally:
		lookaround.stop()

	chiSay = robot.say_text("Chi", in_parallel=True)
	time.sleep(0.2)
	chiMove = robot.set_lift_height(0, in_parallel=True, duration=0.5)
	chiMove.wait_for_completed()
	chiSay.wait_for_completed()

	robot.set_lift_height(0).wait_for_completed()
	robot.set_lift_height(1).wait_for_completed()
	robot.set_lift_height(0).wait_for_completed()




cozmo.run_program(chifoumi)
