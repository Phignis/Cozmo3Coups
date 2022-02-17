#!/usr/bin/python3

import cozmo
import time
import asyncio.tasks
from robotchifoumi import RobotChifoumi
from chifoumi import *

def chifoumi(robotCozmo: cozmo.robot.Robot):
	robotCozmo.enable_stop_on_cliff(True)

	robot = RobotChifoumi(robotCozmo)
	game = GameChifoumi()

	teteJoueur = robot.find_someone_to_play(dureeMax=20)
	if (not teteJoueur):
		#robot.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
		return

	robot.react_start_game(teteJoueur)

	while not game.is_game_ended():
		round_result = robot.play_round(game, teteJoueur)
		
		robot.react_to_round_end(round_result)
		print(game.scoreJ2, " ", game.scoreJ2)
	
	robot.react_to_game_end(game.scoreJ1, game.scoreJ2)


def testWin(robot: cozmo.robot.Robot):
	gameEnded(robot, 0,3)
	gameEnded(robot, 1,3)
	gameEnded(robot, 2,3)
	gameEnded(robot, 3,0)
	gameEnded(robot, 3,1)
	gameEnded(robot, 3,2)


cozmo.run_program(chifoumi, use_viewer=True)
