import cozmo

from random import randint


class DetectionCoupJoueurRandom:

	def __init__(self, robot):
		self.robot = robot

	def wait_for_completed(self):
		pass

	def getResult(self):
		return randint(0, 2)


class DetectionCoupJoueurCube:
	def __init__(self, robot, cubes):
		self.robot = robot
		self.cubes = cubes

	def wait_for_completed(self):
		pass

	def getResult(self):
		return randint(0, 2)

