import tkinter as tk
from tkinter import *
from Game import Game
from serial import Serial
import asyncio
import threading
import re
# set font sizes
LARGE_FONT = ("system", 20)
MED_FONT = ("system", 12)
SMALL_FONT = ("system", 8)


class Application(tk.Tk):
	def __init__(self,loop):
		self.loop=loop
		tk.Tk.__init__(self,*args,**kwargs)
		container = tk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.ser=Serial("/dev/ttyACM0",2000000,timeout=0.5)

		self.frames = {}

		self.game = Game()

		# holds CPU move information to be displayed in CPUMovePage
		self.move = StringVar()
		self.move.set( "e2")
		# holds winner information to be displayed in GameOverPage
		self.winner = StringVar()
		self.winner.set("CPU Wins!")

		# Give page objects to Application to show frame
		for F in (StartGamePage, InitializeBoardPage,SetBoardPage, ChooseColorPage,
				ChooseDifficultyPage, CPUMovePage, PlayerMovePage, CheckPage,
				CPUMoveErrorPage, GameOverPage, PlayerMoveErrorPage, ChoosePromotionPage):

			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky = "nsew")

		self.show_frame(StartGamePage)


	def show_frame(self,cont):

		frame = self.frames[cont]
		frame.tkraise()
	def show_CPU_frame(self,cont,controller):
		frame=self.frames[cont]
		frame.tkraise()

	def send_data(self, controller):
		startPos,endPos=findIndex(controller.game.getCPUMove())
		self.ser.write(controller.game.getCPUMove()+str(controller.game.is_Empty(endPos))+"\n".decode("utf-8"))
		threading.Thread(target=self.wait_for_completion(controller)).start()

	def wait_loop(self):
		data=self.ser.readLineUntil("\n").decode("utf-8").rstrip()
		self.ser.reset_input_buffer()
		x = re.search("Done", data)
		if(x):
			time.sleep(17)
			self.validate_move(controller)
		else:
			self.wait_loop(self)

	def wait_for_completion(self,controller):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.create_task(wait_loop)
		loop.run_until_complete()

	def validate_move(self, controller):

		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.show_frame(GameOverPage)

		elif controller.game.isCheck:
			controller.show_frame(CheckPage)

		elif controller.game.CPUMoveError:
			controller.game.current = controller.game.previous
			controller.show_CPU_frame(CPUMoveErrorPage)
			controller.send_data(controller)

		else:
			controller.show_frame(PlayerMovePage)

class StartGamePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		
		# set label
		label = tk.Label(self,text = "Welcome to Chessmate", font = LARGE_FONT)
		label.pack(pady = 20, padx = 20)

		# set button that takes you to InitializeBoardPage and calls Game.setUp()
		startGameButton = tk.Button(self, text = "Start New Game",font = MED_FONT,
						command = lambda: [controller.show_frame(InitializeBoardPage), controller.game.setUp()])
		startGameButton.pack()


class InitializeBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Please empty the board for calibration", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		initBoardButton = tk.Button(self, text = "Done",font = MED_FONT, command = lambda : [controller.show_frame(SetBoardPage), controller.game.analyzeBoard()])
		initBoardButton.pack()

class ChooseColorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		
		# set label
		label = tk.Label(self,text = "Please select the colour you want to play", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that takes you to CPUMovePage since they will be going first
		# gets move from CPU and displays it in the next window
		blackButton = tk.Button(self, text = "Black",font = MED_FONT,
					command = lambda : [controller.show_CPU_frame(CPUMovePage),controller.move.set(controller.game.CPUMove())])
		blackButton.pack()

		# set button that takes you the PlayerMovePage since user will be going first
		whiteButton = tk.Button(self, text = "White",font = MED_FONT,
					command = lambda: controller.show_frame(PlayerMovePage))
		whiteButton.pack()

class SetBoardPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Calibration done. Now you can place pieces on board", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that takes you to ChooseDifficultyPage and has Game take a picture of the set Board
		setBoardButton = tk.Button(self, text = "Done",font = MED_FONT,
						 command = lambda : [controller.show_frame(ChooseDifficultyPage),controller.game.checkBoardIsSet()])
		setBoardButton.pack()

class PlayerMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Place Your Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that updates player move and checks the moves validity and board circumstances
		PlayerButton = tk.Button(self, text = "Done",font = MED_FONT,
						command = lambda : [controller.game.playerMove(),self.validate_move(controller)])

		# set button that ends game. Shows game over page with CPU as winner
		ResignButton = tk.Button(self, text = "Resign?",font = SMALL_FONT,
						command = lambda : controller.show_frame(GameOverPage))
		PlayerButton.pack()
		ResignButton.pack()

	def validate_move(self,controller):

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
			controller.show_CPU_frame(CPUMovePage)
			controller.send_data(controller)

class CPUMovePage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "CPU Moves:", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set dynamic label with CPU move
		self.moveLabel = tk.Label(self, textvariable = controller.move, font = MED_FONT)
		self.moveLabel.pack(pady = 10, padx = 10)

		# Send Move

		#Wait till done


		# set button that updates photos of board after user moves CPU piece. Checks validity of movement
		CPUButton = tk.Button(self, text = "Done",font = MED_FONT,
						command = lambda : [controller.game.updateCurrent(), self.validate_move(controller)])
		CPUButton.pack()

	def validate_move(self,controller):

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

class CheckPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "You are in Check", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that shows PlayerMovePage
		setBoardButton = tk.Button(self, text = "Continue",font = MED_FONT,
								command = lambda : controller.show_frame(PlayerMovePage))
		setBoardButton.pack()

class CPUMoveErrorPage(tk.Frame):
	'''
	Alerts user that the move they made is not the same as the CPU requested
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "CPU Move was not placed correctly", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that shows CPUMovePage
		setBoardButton = tk.Button(self, text = "Try Again?",font = MED_FONT,
						command = lambda : controller.show_frame(CPUMovePage))
		setBoardButton.pack()


class PlayerMoveErrorPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Invalid Move", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that shows the PlayerMovePage
		setBoardButton = tk.Button(self, text = "Try Again?", font = MED_FONT,
						command = lambda : controller.show_frame(PlayerMovePage))
		setBoardButton.pack()

class GameOverPage(tk.Frame):
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

class ChooseDifficultyPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Choose the difficulty")
		label.pack(pady = 10, padx = 10)

		EasyButton = tk.Button(self, text = "Beginner",
						command = lambda : [self.setEasy(controller), controller.show_frame(ChooseColorPage)])
		EasyButton.pack()

		IntermediateButton = tk.Button(self, text = "Intermediate",
						command = lambda : [self.setIntermediate(controller), controller.show_frame(ChooseColorPage)])
		IntermediateButton.pack()

		HardButton = tk.Button(self, text = "Expert",
						command = lambda : [self.setHard(controller), controller.show_frame(ChooseColorPage)])
		HardButton.pack()


		ExtremeButton = tk.Button(self, text = "Master",
						command = lambda : [self.setExtreme(controller), controller.show_frame(ChooseColorPage)])

		ExtremeButton.pack()

		MasterButton = tk.Button(self, text = "Grandmaster",
						command = lambda : [self.setMaster(controller), controller.show_frame(ChooseColorPage)])

		MasterButton.pack()
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
		
		
		
		
		
class ChoosePromotionPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Which piece do you want to promote?")
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
		controller.game.board.promotion = 'n'
		controller.game.board.move = controller.game.board.move + 'n'
		controller.game.playerPromotion(controller.game.board.move)

		if controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.show_frame(PlayerMoveErrorPage)
		else:
			controller.move.set(controller.game.CPUMove())
			controller.show_frame(CPUMovePage)
	


loop=asyncio.get_event_loop()
app = Application(loop)
app.mainloop()