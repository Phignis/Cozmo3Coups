#!/usr/bin/python3

import cozmo
import time
import asyncio.tasks
import face_images

from cozmo.util import distance_mm, speed_mmps
from random import randint
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
	robot.set_lift_height(0.9).wait_for_completed()

	moveSay = robot.say_text(nomMovement, in_parallel=True, duration_scalar=0.8)
	time.sleep(0.5)
	moveMove = robot.set_lift_height(0, in_parallel=True, duration=0.5)
	moveMove.wait_for_completed()
	moveSay.wait_for_completed()

def movement_chifoumi(robot: cozmo.robot.Robot):
	move_lift_and_say(robot, "Chi")
	move_lift_and_say(robot, "Fou")
	move_lift_and_say(robot, "Mi")

def displayCoupCozmo(robot: cozmo.robot.Robot, coupCozmo, duration):
	if coupCozmo==0:
		img = images["Chi"]
	elif coupCozmo==1:
		img = images["Fou"]
	else:
		img = images["Mi"]
	return robot.display_oled_face_image(img, duration, in_parallel=True)


class DetectionCoupJoueur:
	def wait_for_completed(self):
		pass

	def getResult(self):
		return randint(0,2)

def detectJoueurCoup(robot, tete):
	return DetectionCoupJoueur()

def resultatManche(coup1, coup2):
	# 0>1>2>0
	# 0-1 = -1	a
	# 1-0 = 1	b
	# 0-2 = -2	b
	# 2-0 = 2	a
	# 1-2 = -1	a
	# 2-1 = 1	b	
	dif = coup1-coup2
	if (dif == 0):
		return 0
	elif (dif==-1 or dif == 2):
		return 1
	else:
		return -1 


def jouerManche(robot: cozmo.robot.Robot):
	movement_chifoumi(robot)

	coupCozmo = randint(0,2)
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel=True)
	detectionCoupJoueur = detectJoueurCoup(robot, teteJoueur)
	displayCoupC = displayCoupCozmo(robot, coupCozmo, 2000)
	detectionCoupJoueur.wait_for_completed()
	displayCoupC.wait_for_completed()

	coupJoueur = detectionCoupJoueur.getResult()
	print("Coup joueur : {}".format(coupJoueur))
	resultat = resultatManche(coupCozmo, coupJoueur)
	if resultat == -1:
		robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
	elif resultat == 1:
		robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseRound).wait_for_completed()
	else:
		robot.play_anim_trigger(cozmo.anim.Triggers.DizzyShakeLoop).wait_for_completed()


def chifoumi(robot: cozmo.robot.Robot):
	robot.enable_stop_on_cliff(True)
	robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()

	teteJoueur = find_someone_to_play(robot)
	if (not teteJoueur):
		return

	# Reation à la detection du joueur
	robot.turn_towards_face(teteJoueur).wait_for_completed()
	robot.play_anim_trigger(cozmo.anim.Triggers.RequestGameMemoryMatchAccept0).wait_for_completed()
	
	jouerManche(robot)
	


cozmo.run_program(chifoumi, use_viewer=True)
