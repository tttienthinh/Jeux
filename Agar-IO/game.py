import pygame
from client import Network
import random
import os

from function import *
from constant import *



def main(name):
	"""
	function for running the game,
	includes the main loop of the game

	:param name: the my_player name
	"""
	# start by connecting to the network
	server = Network()
	my_id = server.connect(name)
	balls, players, game_time = server.send("get")

	# setup the clock, limit to 30fps
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30) # 30 fps max
		my_player = players[my_id]
		vel = START_VEL - round(my_player["score"]/14)
		if vel <= 1:
			vel = 1



		# get mouse position
		mouse_pos = pygame.mouse.get_pos()
		
		print(mouse_pos[0] - my_player["x"], mouse_pos[1] - my_player["y"])
		#movement based on mouse position
		if mouse_pos[0] - my_player["x"] < 0:
			if my_player["x"] - vel - PLAYER_RADIUS - my_player["score"] >= 0:
				my_player["x"] = my_player["x"] - vel

		if mouse_pos[0] - my_player["x"] > 0:
			if my_player["x"] + vel + PLAYER_RADIUS + my_player["score"] <= W:
				my_player["x"] = my_player["x"] + vel

		if mouse_pos[1] - my_player["y"] < 0:
			if my_player["y"] - vel - PLAYER_RADIUS - my_player["score"] >= 0:
				my_player["y"] = my_player["y"] - vel

		if mouse_pos[1] - my_player["y"] > 0:
			if my_player["y"] + vel + PLAYER_RADIUS + my_player["score"] <= H:
				my_player["y"] = my_player["y"] + vel
		
		
		data = "move " + str(my_player["x"]) + " " + str(my_player["y"])
		# send data to server and recieve back all players information
		balls, players, game_time = server.send(data)

		for event in pygame.event.get():
			# if user hits red x button close window
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				# if user hits a escape key close program
				run = False


		# redraw window then update the frame
		redraw_window(my_player, players, balls, game_time, 
				  WIN, PLAYER_RADIUS, BALL_RADIUS, 
				  NAME_FONT, TIME_FONT, SCORE_FONT, W, H)
		pygame.display.update()


	server.disconnect()
	pygame.quit()
	quit()

# get users name
# name = get_name()
name = "TT"
name = "01234567890123456789"
name = "0123456789012345678"

# make window start in top left hand corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

# setup pygame window
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Blobs")

# start game
main(name)