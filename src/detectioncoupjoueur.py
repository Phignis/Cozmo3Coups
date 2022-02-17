
import cozmo
from random import randint


class DetectionCoupJoueurRandom:

	def __init__(self, robot, tete):
		self.robot = robot
		self.tete = tete

	def wait_for_completed(self):
		pass

	def getResult(self):
		return randint(0,2)

