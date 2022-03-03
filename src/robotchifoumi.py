import cozmo
import time
import asyncio.tasks
from cozmo.util import distance_mm, speed_mmps, degrees
from random import randint
from detectioncoupjoueur import DetectionCoupJoueurRandom
import face_images
from chifoumi import Coup, RoundResult, GameChifoumi

import os


class RobotChifoumi:
	def __init__(self, robot: cozmo.robot.Robot):
		self.robot = robot

		current_directory = os.path.dirname(os.path.realpath(__file__))
		self.images = {
			Coup.ROCK: face_images.load_cozmo_image(os.path.join(current_directory, "../image/chi.png")),
			Coup.PAPER: face_images.load_cozmo_image(os.path.join(current_directory, "../image/fou.png")),
			Coup.SCISSORS: face_images.load_cozmo_image(os.path.join(current_directory, "../image/mi.png"))
		}

	def find_someone_to_play(self, dureeMax=10):
		try:
			lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
			tetePersonne = self.robot.world.wait_for_observed_face(timeout=dureeMax)
			lookaround.stop()
			return tetePersonne
		except asyncio.tasks.futures.TimeoutError:
			lookaround.stop()
			return None


	def play_round(self, game : GameChifoumi, teteJoueur) -> RoundResult:
		self.robot.turn_towards_face(teteJoueur).wait_for_completed()
		self.movement_chifoumi()

		coupCozmo = self.get_coup()
		self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel=True)
		detectionCoupJoueur = self.detect_joueur_coup(teteJoueur)
		displayCoupC = self.display_coup(coupCozmo, 2000)
		detectionCoupJoueur.wait_for_completed()
		displayCoupC.wait_for_completed()

		coupJoueur = detectionCoupJoueur.getResult()
		print("Coup joueur : {}".format(coupJoueur))
		return game.play_round(coupCozmo, coupJoueur)

	def react_start_game(self, tete_joueur):
		self.robot.turn_towards_face(tete_joueur).wait_for_completed()
		self.robot.play_anim_trigger(cozmo.anim.Triggers.RequestGameMemoryMatchAccept0).wait_for_completed()

	def react_to_inactive_player(self):
		self.robot.play_anim_trigger(cozmo.anim.Triggers.Singing_120bpm).wait_for_completed()
		self.robot.say_text("Joue ton coup, je n'en peux plus d'attendre").wait_for_completed()

	
	def get_coup(self) -> Coup:
		r = randint(0, 2)
		if r == 0:
			return Coup.ROCK
		elif r == 1:
			return Coup.PAPER
		else:
			return Coup.SCISSORS	

	def detect_joueur_coup(self) -> DetectionCoupJoueurRandom:
		return DetectionCoupJoueurRandom(self.robot)

	def move_lift_and_say(self, nomMovement):
		self.robot.set_lift_height(0.9).wait_for_completed()

		moveSay = self.robot.say_text(nomMovement, in_parallel=True, duration_scalar=0.8)
		time.sleep(0.5)
		moveMove = self.robot.set_lift_height(0, in_parallel=True, duration=0.5)
		moveMove.wait_for_completed()
		moveSay.wait_for_completed()

	def movement_chifoumi(self):
		self.move_lift_and_say("Chi")
		self.move_lift_and_say("Fou")
		self.move_lift_and_say("Mi")


	def display_coup(self, coupCozmo : Coup, duration):
		return self.robot.display_oled_face_image(self.images[coupCozmo], duration, in_parallel=True)

	def react_to_round_end(self, result : RoundResult):
		if result == RoundResult.PLAYER1_WIN:
			self.robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinRound).wait_for_completed()
		elif result == RoundResult.PLAYER2_WIN:
			self.robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseRound).wait_for_completed()
		else:
			self.robot.play_anim_trigger(cozmo.anim.Triggers.DizzyShakeStop).wait_for_completed()


	def react_to_game_end(self, scoreCozmo, scoreJoueur):
		if scoreCozmo == 3:
			if scoreJoueur == 0:
				self.robot.say_text("Ah! ah! ah! 3 0").wait_for_completed()
			elif scoreJoueur == 1:
				self.robot.say_text("3 1 ! 3 1 !").wait_for_completed()
			else: # scoreJoueur == 2
				self.robot.say_text("Bien joué mais j'ai gagné 3 2").wait_for_completed()
			
			self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin ).wait_for_completed()
		
		else: # Joueur a gagné
			if scoreCozmo == 0:
				self.robot.say_text("Tricheur! 0 3").wait_for_completed()
			elif scoreCozmo == 1:
				self.robot.say_text("1 3").wait_for_completed()
			else: # scoreCozmo == 2
				self.robot.say_text("Bien joué, 2 3").wait_for_completed()
			
			self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()

