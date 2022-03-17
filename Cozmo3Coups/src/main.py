#!/bin/python3

import cozmo
import os
import time
import asyncio.tasks
import sys

import cube_recognition
from robotchifoumi import RobotChifoumi
from chifoumi import *


def main_chifoumi(robot_cozmo: cozmo.robot.Robot, nb_point_gagnant):
    robot_cozmo.world.auto_disconnect_from_cubes_at_end(
        enable=True)  # all cubes will disconnect after the end of program

    robot_cozmo.enable_stop_on_cliff(True)

    robot = RobotChifoumi(robot_cozmo)
    game = GameChifoumi(nb_point_gagnant)

    tete_joueur = robot.find_someone_to_play(duree_max=30)
    if not tete_joueur:
        robot_cozmo.say_text("Personne ne veux jouer avec moi !").wait_for_completed()
        return

    robot.react_start_game(tete_joueur)

    if not cube_recognition.connect_to_light_cubes(robot.robot):
        return
    else:
        for cube in robot.robot.world.connected_light_cubes:
            cube_recognition.light_cube_identification(cube)

    while not game.is_game_ended():
        try:
            round_result = robot.play_round(game, tete_joueur)
        except asyncio.TimeoutError:
            robot.robot.say_text("Tu ne joues plus, j'en ai marre j'arrête!").wait_for_completed()
            robot.robot.play_anim_trigger(cozmo.anim.Triggers.NothingToDoBoredEvent).wait_for_completed()
            return 2

        robot.react_to_round_end(round_result)
        print(game.scoreJ1, " ", game.scoreJ2)

    robot.react_to_game_end(game.scoreJ1, game.scoreJ2)

    for cube in robot.robot.world.connected_light_cubes:
        cube.set_lights_off()


nb_point_gagnant = 3

if len(sys.argv) == 2:
    nb_point_gagnant = int(sys.argv[1])

print(nb_point_gagnant)

cozmo.run_program(lambda r: main_chifoumi(r, nb_point_gagnant), use_viewer=True)
