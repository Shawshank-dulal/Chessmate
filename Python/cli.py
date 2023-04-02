from Game import Game
import time
class cli():
    def __init__(self,*args,**kwargs):
        self.frames = {}
        self.game = Game()
		# holds CPU move information to be displayed in CPUMovePage
        self.move.set( "e2")
		# holds winner information to be displayed in GameOverPage
        self.winner = StringVar()
        self.winner.set("CPU Wins!")
        self.StartGamePage()



class StartGamePage():
    def __init__(self, parent, controller):
        self.controller = controller
        self.controller.game.setUp()
        print("Starting Game")


class InitializeBoardPage():
	'''
	Prompts player to clear board so the board may be initialized
	'''

	def __init__(self,parent,controller):

            controller.game.analyzeBoard()
            inp=input("is the board clear for calibration? (y/n)")
            if inp == "y":
                controller.game.clearBoard()
                controller.game.setUp()
            else:
                controller.game.setUp()
class ChooseColorPage():
	'''
	Prompts player to choose color and shows appropriate window for first move
	'''

	def __init__(self,parent,controller):
         inp=input("Choose Color w/b?")
         if inp == "b":
            controller.game.CPUMove()
         elif inp=="w":
            controller.game.PlayerMove()
         else:
            print("Invalid Input")
            controller.game.chooseColor()
		# tk.Frame.__init__(self,parent)
		
		# # set label
		# label = tk.Label(self,text = "Which color would you like to play?", font = LARGE_FONT)
		# label.pack(pady = 10, padx = 10)
 
		# # set button that takes you to CPUMovePage since they will be going first
		# # gets move from CPU and displays it in the next window
		# blackButton = tk.Button(self, text = "Red (Black)",font = MED_FONT,
		# 			command = lambda : [controller.show_frame(CPUMovePage),controller.move.set(controller.game.CPUMove())])
		# blackButton.pack()

		# # set button that takes you the PlayerMovePage since user will be going first
		# whiteButton = tk.Button(self, text = "Blue (White)",font = MED_FONT,
		# 			command = lambda: controller.show_frame(PlayerMovePage))
		# whiteButton.pack()

class SetBoardPage():
	'''
	Prompts user to set board after initialization
	'''

	def __init__(self,parent,controller):
         self.controller=controller
		# # tk.Frame.__init__(self,parent)

		# # set label
		# label = tk.Label(self,text = "Game Initialization Done. Set Board", font = LARGE_FONT)
		# label.pack(pady = 10, padx = 10)

		# # set button that takes you to ChooseDifficultyPage and has Game take a picture of the set Board
		# setBoardButton = tk.Button(self, text = "Done",font = MED_FONT,
		# 				 command = lambda : [controller.show_frame(ChooseDifficultyPage),controller.game.checkBoardIsSet()])
		# setBoardButton.pack()
         label = "Game Initialization Done. Set Board"
         print(label)
         difficulty = input("Enter The game difficulty i.e Medium=M,Easy=E,Difficult=D")
         controller.game.checkBoardIsSet()
         controller.game.chooseDifficulty(difficulty)


class PlayerMovePage():
	'''
	Prompts player to move
	'''

	def __init__(self,parent,controller):
         resign=input("Would you like to resign? (y/n)")
         if resign == "y":
                controller.game.resign()
                controller.winner.set(controller.game.winner)
                controller.show_frame(GameOverPage)
         else:
                inp=input("Enter your move")
                controller.game.playerMove(inp)
                self.checkValid(controller)

def checkValid(self,controller):
		'''
		Performs various checks on move validity and board circumstances.
		Shows the appropriate window given the conditions
		'''

		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.show_frame(GameOverPage)

		elif controller.game.board.promo:
			controller.show_frame(ChoosePromotionPage)

		elif controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)

		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)

class CPUMovePage():
	'''
	Displays chess engine move and prompts user to move piece
	'''

	def __init__(self,parent,controller):
            print("CPU Moves",controller.game.updateCurrent())
            self.checkValid(controller)

		# tk.Frame.__init__(self,parent)

		# # set label
		# label = tk.Label(self,text = "CPU Move:", font = LARGE_FONT)
		# label.pack(pady = 10, padx = 10)

		# # set dynamic label with CPU move
		# self.moveLabel = tk.Label(self, textvariable = controller.move, font = MED_FONT)
		# self.moveLabel.pack(pady = 10, padx = 10)

		# # set button that updates photos of board after user moves CPU piece. Checks validity of movement
		# CPUButton = tk.Button(self, text = "Done",font = MED_FONT,
		# 				command = lambda : [controller.game.updateCurrent(), self.checkValid(controller)])
		# CPUButton.pack()

def checkValid(self,controller):
		'''
		Performs various checks on move validity and board circumstances.
		Shows the appropriate window given the conditions
		'''
		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.show_frame(GameOverPage)

		elif controller.game.isCheck:
			controller.show_frame(CheckPage)

		elif controller.game.CPUMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(CPUMoveErrorPage)

		else:
			controller.show_frame(PlayerMovePage)

class CheckPage():
	'''
	Alerts user they are in check
	'''

	def __init__(self,parent,controller):
         print("You are in check...")
         controller.PlayerMovePage()

		# tk.Frame.__init__(self,parent)

		# # set label
		# label = tk.Label(self,text = "You are in Check", font = LARGE_FONT)
		# label.pack(pady = 10, padx = 10)

		# # set button that shows PlayerMovePage
		# setBoardButton = tk.Button(self, text = "Proceed",font = MED_FONT,
		# 						command = lambda : controller.show_frame(PlayerMovePage))
		# setBoardButton.pack()

class CPUMoveErrorPage():
	'''
	Alerts user that the move they made is not the same as the CPU requested
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "That was not the correct CPU move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that shows CPUMovePage
		setBoardButton = tk.Button(self, text = "Try Again",font = MED_FONT,
						command = lambda : controller.show_frame(CPUMovePage))
		setBoardButton.pack()


class PlayerMoveErrorPage():
	'''
	Alerts the user they made an invalid move
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Error Invalid Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that shows the PlayerMovePage
		setBoardButton = tk.Button(self, text = "Try Again", font = MED_FONT,
						command = lambda : controller.show_frame(PlayerMovePage))
		setBoardButton.pack()

class GameOverPage():
	'''
	Shows the winner of the game
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Game Over", font = LARGE_FONT)

		# set dynamic label that will update with the game winner
		self.winnerLabel = tk.Label(self, textvariable = controller.winner, font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		self.winnerLabel.pack(pady = 10, padx = 10)

class ChooseDifficultyPage():
	'''
	Prompts user to pick a difficulty for the chess engine
	'''

	def __init__(self,parent,controller):

		# tk.Frame.__init__(self,parent)
		# label = tk.Label(self,text = "Choose the difficulty")
		# label.pack(pady = 10, padx = 10)

		# EasyButton = tk.Button(self, text = "Easy",
		# 				command = lambda : [self.setEasy(controller), controller.show_frame(ChooseColorPage)])
		# EasyButton.pack()

		# IntermediateButton = tk.Button(self, text = "Intermediate",
		# 				command = lambda : [self.setIntermediate(controller), controller.show_frame(ChooseColorPage)])
		# IntermediateButton.pack()

		# HardButton = tk.Button(self, text = "Hard",
		# 				command = lambda : [self.setHard(controller), controller.show_frame(ChooseColorPage)])
		# HardButton.pack()


		# ExtremeButton = tk.Button(self, text = "Extreme",
		# 				command = lambda : [self.setExtreme(controller), controller.show_frame(ChooseColorPage)])

		# ExtremeButton.pack()

		# MasterButton = tk.Button(self, text = "Master",
		# 				command = lambda : [self.setMaster(controller), controller.show_frame(ChooseColorPage)])

		# MasterButton.pack()
		pass

	def setEasy(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 1})

	def setIntermediate(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 5})

	def setHard(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 10})

	def setExtreme(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 15})

	def setMaster(self,controller):
		controller.game.chessEngine.engine.setoption({'Skill Level' : 20})
		
		
		
		
		
class ChoosePromotionPage():
	'''
	Prompts user to choose to which piece they would like to promote their pawn
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Choose your promotion")
		label.pack(pady = 10, padx = 10)

		QueenButton = tk.Button(self, text = "Queen",
						command = lambda : [self.setQueen(controller)])

		RookButton = tk.Button(self, text = "Rook",
						command = lambda : [self.setRook(controller)])

		BishopButton = tk.Button(self, text = "Bishop",
						command = lambda : [self.setBishop(controller)])
	
		KnightButton = tk.Button(self, text = "Knight",
						command = lambda : [self.setKnight(controller)])
		QueenButton.pack()
		RookButton.pack()
		BishopButton.pack()
		KnightButton.pack()
		
	def setQueen(self,controller):
		'''
		Updates the move to UCI recognized move for promotion
		Checks validity
		'''

		controller.game.board.promotion = 'q'
		controller.game.board.move = controller.game.board.move + 'q'
		controller.game.playerPromotion(controller.game.board.move)

		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	def setRook(self,controller):
		'''
		Updates the move to UCI recognized move for promotion
		Checks validity. Updates board
		'''

		controller.game.board.promotion = 'r'
		controller.game.board.move = controller.game.board.move + 'r'
		controller.game.playerPromotion(controller.game.board.move)

		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	
	def setBishop(self,controller):
		'''
		Updates the move to UCI recognized move for promotion
		Checks validity. Updates board
		'''

		controller.game.board.promotion = 'b'
		controller.game.board.move = controller.game.board.move + 'b'
		controller.game.playerPromotion(controller.game.board.move)

		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	
	def setKnight(self,controller):
		'''
		Updates the move to UCI recognized move for promotion
		Checks validity. Updates board
		'''
		controller.game.board.promotion = 'n'
		controller.game.board.move = controller.game.board.move + 'n'
		controller.game.playerPromotion(controller.game.board.move)

		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
