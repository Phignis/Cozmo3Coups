#!/usr/bin/python3

import cozmo
import time
import asyncio.tasks
from robotchifoumi import RobotChifoumi
from chifoumi import *


def main_chifoumi(robot_cozmo: cozmo.robot.Robot):

	robot_cozmo.world.auto_disconnect_from_cubes_at_end(enable=True)  # all cubes will disconnect after the end of program

	robot_cozmo.enable_stop_on_cliff(True)

	robot = RobotChifoumi(robot_cozmo)
	game = GameChifoumi()

	tete_joueur = robot.find_someone_to_play(dureeMax=20)
	if not tete_joueur:
		# robot.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
		return

	robot.react_start_game(tete_joueur)

	while not game.is_game_ended():
		round_result = robot.play_round(game, tete_joueur)
		
		robot.react_to_round_end(round_result)
		print(game.scoreJ2, " ", game.scoreJ2)
	
	robot.react_to_game_end(game.scoreJ1, game.scoreJ2)


cozmo.run_program(main_chifoumi, use_viewer=True)
