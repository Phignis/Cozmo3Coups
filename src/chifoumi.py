#!/usr/bin/python3

import cozmo
import time
import asyncio.tasks
import face_images

from cozmo.util import distance_mm, speed_mmps

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
images = {
	"Chi": face_images.load_cozmo_image(os.path.join(current_directory, "../image/chi.png")),
	"Fou": face_images.load_cozmo_image(os.path.join(current_directory, "../image/fou.png")),
	"Mi": face_images.load_cozmo_image(os.path.join(current_directory, "../image/mi.png")) 
}


def find_someone_to_play(robot: cozmo.robot.Robot):
	try:
		lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
		tetePersonne = robot.world.wait_for_observed_face(timeout=10)
		lookaround.stop()
		return tetePersonne
	except asyncio.tasks.futures.TimeoutError:
		lookaround.stop()
		robot.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
		return None

def move_lift_and_say(robot: cozmo.robot.Robot, nomMovement):
	robot.set_lift_height(1).wait_for_completed()

	moveSay = robot.say_text(nomMovement, in_parallel=True, duration_scalar=0.8)
	time.sleep(0.5)
	moveMove = robot.set_lift_height(0, in_parallel=True, duration=0.5)
	moveMove.wait_for_completed()
	moveSay.wait_for_completed()

def movement_chifoumi(robot: cozmo.robot.Robot):
	move_lift_and_say(robot, "Chi")
	move_lift_and_say(robot, "Fou")
	move_lift_and_say(robot, "Mi")



def chifoumi(robot: cozmo.robot.Robot):
	robot.enable_stop_on_cliff(True)
	robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()


	if (not find_someone_to_play(robot)):
		return


	movement_chifoumi(robot)

	
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	robot.display_oled_face_image(images["Chi"], 3000).wait_for_completed()
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	robot.display_oled_face_image(images["Fou"], 3000).wait_for_completed()
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
	robot.display_oled_face_image(images["Mi"], 3000).wait_for_completed()





cozmo.run_program(chifoumi)
