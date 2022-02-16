#!/usr/bin/python3

import cozmo
import time
import asyncio.tasks
import face_images

from cozmo.util import distance_mm, speed_mmps, degrees
from random import randint
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
images = {
	"Chi": face_images.load_cozmo_image(os.path.join(current_directory, "../image/chi.png")),
	"Fou": face_images.load_cozmo_image(os.path.join(current_directory, "../image/fou.png")),
	"Mi": face_images.load_cozmo_image(os.path.join(current_directory, "../image/mi.png")) 
}


def find_someone_to_play(robot: cozmo.robot.Robot, dureeMax=10):
	try:
		lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
		tetePersonne = robot.world.wait_for_observed_face(timeout=dureeMax)
		lookaround.stop()
		return tetePersonne
	except asyncio.tasks.futures.TimeoutError:
		lookaround.stop()
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


def jouerManche(robot: cozmo.robot.Robot, teteJoueur):
	movement_chifoumi(robot)

	coupCozmo = randint(0,2)
	robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel=True)
	detectionCoupJoueur = detectJoueurCoup(robot, teteJoueur)
	displayCoupC = displayCoupCozmo(robot, coupCozmo, 2000)
	detectionCoupJoueur.wait_for_completed()
	displayCoupC.wait_for_completed()

	coupJoueur = detectionCoupJoueur.getResult()
	print("Coup joueur : {}".format(coupJoueur))
	return resultatManche(coupCozmo, coupJoueur)
	
def finDeManche(robot: cozmo.robot.Robot, resultat, scoreCozmo, scoreJoueur):
	if resultat == -1:
		scoreCozmo += 1
		robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
	elif resultat == 1:
		scoreJoueur += 1
		robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseRound).wait_for_completed()
	else:
		robot.play_anim_trigger(cozmo.anim.Triggers.DizzyShakeStop).wait_for_completed()
	
	return scoreCozmo, scoreJoueur

def gameEnded(robot: cozmo.robot.Robot, scoreJoueur, scoreCozmo):
	if scoreCozmo == 3:
		if scoreJoueur == 0:
			robot.say_text("Ah! ah! ah! 3 0").wait_for_completed()
		elif scoreJoueur == 1:
			robot.say_text("3 1 ! 3 1 !").wait_for_completed()
		else: # scoreJoueur == 2
			robot.say_text("Bien joué mais j'ai gagné 3 2").wait_for_completed()
		
		robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin ).wait_for_completed()
	 
	else: # Joueur a gagné
		if scoreCozmo == 0:
			robot.say_text("Tricheur! 0 3").wait_for_completed()
		elif scoreCozmo == 1:
			robot.say_text("1 3").wait_for_completed()
		else: # scoreCozmo == 2
			robot.say_text("Bien joué, 2 3").wait_for_completed()
		
		robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()

def chifoumi(robot: cozmo.robot.Robot):
	robot.enable_stop_on_cliff(True)

	p = cozmo.util.Pose(0,0,0, angle_z=degrees(0))

	teteJoueur = find_someone_to_play(robot, dureeMax=20)
	if (not teteJoueur):
		#robot.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
		return

	# Reation à la detection du joueur
	robot.turn_towards_face(teteJoueur).wait_for_completed()
	robot.play_anim_trigger(cozmo.anim.Triggers.RequestGameMemoryMatchAccept0).wait_for_completed()
	
	scoreJoueur = 0
	scoreCozmo = 0

	while scoreJoueur != 3 and scoreCozmo != 3:
		robot.go_to_pose(p).wait_for_completed()
		robot.turn_towards_face(teteJoueur).wait_for_completed()
		resultat = jouerManche(robot, teteJoueur)
		
		scoreCozmo, scoreJoueur = finDeManche(robot, resultat, scoreCozmo, scoreJoueur)
		print(scoreCozmo, " ", scoreJoueur)
	
	gameEnded(robot, scoreJoueur, scoreCozmo)


def testWin(robot: cozmo.robot.Robot):
	gameEnded(robot, 0,3)
	gameEnded(robot, 1,3)
	gameEnded(robot, 2,3)
	gameEnded(robot, 3,0)
	gameEnded(robot, 3,1)
	gameEnded(robot, 3,2)


cozmo.run_program(chifoumi, use_viewer=True)
