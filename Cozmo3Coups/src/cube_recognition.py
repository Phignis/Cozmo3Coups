import asyncio
import time

import cozmo
import robotchifoumi


def wait_for_light_cubes(robot: cozmo.robot.Robot, amount_cubes=3, time_searching=5):
    """
    wait_for_light_cubes a pour but de faire rechercher a un robot Cozmo un certain nombre de cubes dans son environnement
    Il se mettra a regarder autour de lui pendant un temps déterminé jusqu'à trouver les cubes voulus

    :param robot: (class:`cozmo.robot.Robot`) Robot  devant rechercher les cubes
    :param time_searching: (float) nombre de secondes durant lequel robot effectue sa recherche. Default: 20
    :param amount_cubes: (int) nombre de cubes devant etre trouvé pour arreter de regarder autour de lui. Default: 3
    :return (int) nombre d'objets trouvés
    """
    try:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        nb_cubes_seen = robot.world.wait_until_num_objects_visible(num=amount_cubes,
                                                                   object_type=cozmo.objects.LightCube,
                                                                   timeout=time_searching)
        print(nb_cubes_seen)
        look_around.stop()
        return nb_cubes_seen
    except asyncio.TimeoutError:  # not enough cubes were found visible at same time
        print(0)
        look_around.stop()
        return 0


def get_light_cubes(robot: cozmo.robot.Robot, amount_cubes=3, time_searching=5):
    """
    Permet de se connecter des lightcubes autour de lui, des 3 types différents
    :param robot: Robot recherchant les cubes
    :param amount_cubes: Le nombre de cubes censé être dans son environnement
    :param time_searching: Le temps passé a rechercher les cubes
    :return: La liste des cubes auquel le robot a pu se connecter
    """
    if wait_for_light_cubes(robot, amount_cubes, time_searching) == amount_cubes:
        if robot.world.connect_to_cubes():
            robot.say_text("on a de quoi jouer", True).wait_for_completed()
            print(robot.world.connected_light_cubes())
        else:
            robot.say_text("je n'arrive pas a me connecter aux cubes").wait_for_completed()
    else:
        robot.say_text("on n'a pas de quoi jouer").wait_for_completed()
        return


def test_wait_for(robot_chi: robotchifoumi.RobotChifoumi):
    print("début")
    robot_chi.robot.world.wait_for(cozmo.objects.EvtObjectTapped)
    print("fin")


def test_inactivity(robot_chi: robotchifoumi.RobotChifoumi):
    robot_chi.react_to_inactive_player()


def launch(robot: cozmo.robot.Robot):
    test_inactivity(robotchifoumi.RobotChifoumi(robot))


cozmo.run_program(launch)
