import cozmo

from random import randint

import chifoumi
import robotchifoumi


class DetectionCoupJoueurRandom:

	def __init__(self, robot_chifoumi):
		self.robot_chifoumi = robot_chifoumi

	def wait_for_completed(self):
		pass

	def getResult(self):
		return randint(0, 2)


class DetectionCoupJoueurCube:
	def __init__(self, robot_chifoumi):
		self.robot_chifoumi = robot_chifoumi

	def get_coup_joueur(self) -> chifoumi.Coup:
		evt = self.robot_chifoumi.robot.world.wait_for(cozmo.objects.EvtObjectTapped)

		r = evt.obj.cube_id

		print("coup joué récupéré : {}".format(r))

		if r == 1:
			return chifoumi.Coup.ROCK
		elif r == 2:
			return chifoumi.Coup.PAPER
		else:
			return chifoumi.Coup.SCISSORS
		# return chifoumi.Coup(evt.obj.cube_id)


