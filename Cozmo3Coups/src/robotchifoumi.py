import cozmo
import time
import asyncio.tasks
from cozmo.util import distance_mm, speed_mmps, degrees
from random import randint

import detectioncoupjoueur
from detectioncoupjoueur import DetectionCoupJoueurRandom
import face_images
from chifoumi import Coup, RoundResult, GameChifoumi

import os


class RobotChifoumi:
    """
    RobotChifoumi représente un robot de notre application. il possède en attribut un robot (cozmo.robot.Robot), et les images
    représentant les coups
    """

    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot

        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.images = {
            Coup.ROCK: face_images.load_cozmo_image(os.path.join(current_directory, "../resources/image/rock.png")),
            Coup.PAPER: face_images.load_cozmo_image(os.path.join(current_directory, "../resources/image/paper.png")),
            Coup.SCISSORS: face_images.load_cozmo_image(os.path.join(current_directory,
                                                                     "../resources/image/scissors.png"))
        }

    def find_someone_to_play(self, duree_max=10):
        try:
            lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.FindFaces)
            tete_personne = self.robot.world.wait_for_observed_face(timeout=duree_max)
            lookaround.stop()
            return tete_personne
        except asyncio.tasks.futures.TimeoutError:
            lookaround.stop()
            return None

    def play_round(self, game: GameChifoumi, tete_joueur) -> RoundResult:
        self.robot.turn_towards_face(tete_joueur).wait_for_completed()
        self.movement_chifoumi()

        coup_cozmo = self.get_coup()
        coup_joueur = detectioncoupjoueur.DetectionCoupJoueurCube(self).get_coup_joueur()

        self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel=True)
        display_coup_c = self.display_coup(coup_cozmo, 2000)
        display_coup_c.wait_for_completed()

        print("Coup joueur : {}, coup cozmo : {}".format(coup_joueur, coup_cozmo))
        return game.play_round(coup_cozmo, coup_joueur)

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

    def move_lift_and_say(self, nom_movement):
        self.robot.set_lift_height(0.9).wait_for_completed()

        moveSay = self.robot.say_text(nom_movement, in_parallel=True, duration_scalar=0.8)
        time.sleep(0.5)
        moveMove = self.robot.set_lift_height(0, in_parallel=True, duration=0.5)
        moveMove.wait_for_completed()
        moveSay.wait_for_completed()

    def movement_chifoumi(self):
        self.move_lift_and_say("Chi")
        self.move_lift_and_say("Fou")
        self.move_lift_and_say("Mi")

    def display_coup(self, coupCozmo: Coup, duration):
        return self.robot.display_oled_face_image(self.images[coupCozmo], duration, in_parallel=True)

    def react_to_round_end(self, result: RoundResult):
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
            else:  # scoreJoueur == 2
                self.robot.say_text("Bien joué mais j'ai gagné 3 2").wait_for_completed()

            self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()

        else:  # Joueur a gagné
            if scoreCozmo == 0:
                self.robot.say_text("Tricheur! 0 3").wait_for_completed()
            elif scoreCozmo == 1:
                self.robot.say_text("1 3").wait_for_completed()
            else:  # scoreCozmo == 2
                self.robot.say_text("Bien joué, 2 3").wait_for_completed()

            self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
