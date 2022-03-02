import asyncio
import time

import cozmo



def get_cube(robot: cozmo.robot.Robot):
    robot.move_head(1.0)
    robot.world.visible_face_count()
    time.sleep(100)


def wait_for_light_cubes(robot: cozmo.robot.Robot, amount_cubes=3, time_searching=5):
    """Recherche un certain nombre de cubes autour de lui pendant un certain temps

        wait_for_light_cubes a pour but de faire rechercher a un robot Cozmo un certain nombre de cubes dans son environnement
        Il se mettra a regarder autour de lui pendant un temps déterminé jusqu'à trouver les cubes voulus

        :param robot: (class:`cozmo.robot.Robot`) Robot  devant rechercher les cubes
        :param time_searching: (float) nombre de secondes durant lequel robot effectue sa recherche. Default: 20
        :param amount_cubes: (int) nombre de cubes devant etre trouvé pour arreter de regarder autour de lui. Default: 3

        :return ([cozmo.objects.LightCube]) une array contenant tout les objets trouvés
    """
    try:
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        nb_cubes_seen = robot.world.wait_until_num_objects_visible(num=amount_cubes,
                                                                   object_type=cozmo.objects.LightCube,
                                                                   timeout=time_searching)
        print(nb_cubes_seen)
        look_around.stop()
    except asyncio.tasks.futures.TimeoutError:  # not enought cubes were found visible at same time
        print(0)
        look_around.stop()
        return 0


cozmo.run_program(wait_for_light_cubes, use_viewer=True)
