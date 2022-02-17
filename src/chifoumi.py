
from enum import Enum

class Coup(Enum):
	ROCK = 1,
	PAPER = 2,
	SCISSORS = 3

class RoundResult(Enum):
	DRAW = 0,
	PLAYER1_WIN = 1,
	PLAYER2_WIN = 2
    
class GameChifoumi:

	def __init__(self, nbPointGagnant=3):
		self.scoreJ1 = 0
		self.scoreJ2 = 0
		self.nbPointGagnant = nbPointGagnant
	
	def get_round_result(self, coup1 : Coup, coup2 : Coup) -> RoundResult:
		if coup1 == coup2:
			return RoundResult.DRAW
		
		if coup1==Coup.ROCK:
			if coup2==Coup.PAPER:
				return RoundResult.PLAYER2_WIN
			elif coup2==Coup.SCISSORS:
				return RoundResult.PLAYER1_WIN

		elif coup1==Coup.PAPER:
			if coup2==Coup.SCISSORS:
				return RoundResult.PLAYER2_WIN
			elif coup2==Coup.ROCK:
				return RoundResult.PLAYER1_WIN

		elif coup1==Coup.SCISSORS:
			if coup2==Coup.ROCK:
				return RoundResult.PLAYER2_WIN
			elif coup2==Coup.PAPER:
				return RoundResult.PLAYER1_WIN


	def play_round(self, coup1 : Coup, coup2 : Coup) -> RoundResult:
		result = self.get_round_result(coup1, coup2)
		
		if result == RoundResult.PLAYER1_WIN:
			scoreJ1 += 1
		elif result == RoundResult.PLAYER2_WIN:
			scoreJ2 += 1

		return result

	def is_game_ended(self) -> bool : 
		return self.scoreJ1==self.nbPointGagnant or self.scoreJ2==self.nbPointGagnant

	def get_winner(self):
		if self.scoreJ1==self.nbPointGagnant:
			return 1
		elif self.scoreJ2==self.nbPointGagnant:
			return 2
		return 0

