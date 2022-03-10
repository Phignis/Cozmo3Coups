import asyncio
import time

import cozmo
import robotchifoumi


def wait_for_light_cubes(robot: cozmo.robot.Robot, amount_cubes=3, time_searching=5):
    """
    wait_for_light_cubes a pour but de faire rechercher a un robot_cozmo Cozmo un certain nombre de cubes dans son environnement
    Il se mettra a regarder autour de lui pendant un temps déterminé jusqu'à trouver les cubes voulus

    :param robot: (class:`cozmo.robot_cozmo.Robot`) Robot  devant rechercher les cubes
    :param time_searching: (float) nombre de secondes durant lequel robot_cozmo effectue sa recherche. Default: 20
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


def connect_to_light_cubes(robot_cozmo: cozmo.robot.Robot, amount_cubes=3, time_searching=10):
    """
    Permet de se connecter des lightcubes autour de lui, des 3 types différents
    :param robot_cozmo: Robot recherchant les cubes
    :param amount_cubes: Le nombre de cubes censé être dans son environnement
    :param time_searching: Le temps passé a rechercher les cubes
    :return: True si le robot_chifoumi a pu se connecter aux trois light_cubes, false sinon
    """

    if wait_for_light_cubes(robot_cozmo, amount_cubes, time_searching) == amount_cubes:
        if robot_cozmo.world.connect_to_cubes():
            robot_cozmo.say_text("on a de quoi jouer", True).wait_for_completed()
            return True
        else:
            robot_cozmo.say_text("je n'arrive pas a me connecter aux cubes").wait_for_completed()
            return False
    else:
        robot_cozmo.say_text("on n'a pas de quoi jouer").wait_for_completed()
        return False


def test_wait_for(robot_chi: robotchifoumi.RobotChifoumi):
    connect_to_light_cubes(robot_chi.robot)
    print("début")
    evt = robot_chi.robot.world.wait_for(cozmo.objects.EvtObjectTapped)
    print(type(evt.obj))
    print("fin")


def test_inactivity(robot_chi: robotchifoumi.RobotChifoumi):
    robot_chi.react_to_inactive_player()
