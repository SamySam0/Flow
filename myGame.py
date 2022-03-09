''' This file contains the main game classes '''
# -------------------------------------------- #


# --- Module imports ---
from random import uniform as random_float, choice as pick_from_list, randint as random_integer
from tkinter import *
from myAdds import *



# --- Game Classes ---

class Virus:
	''' :info: 	  A class used to create an independent living Virus (good or bad ramdomized)
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), floor_y (int) for the floor y coordinates, force_bad (to force the virus to be bad) default : False
		:outputs: No returns from this class '''
	def __init__(self, canvas, floor_y, force_bad = False):

		# Instances:
		self.life = 'alive'
		self.destroyed = False # Used to save calculations/energy when Virus is dead
		self.is_paused = False
		# ---
		self.canvas = canvas
		self.x_pos, self.y_pos = 1940, 500
		self.width, self.height = 96, 106
		self.angular = round(random_float(-0.25, 0.25), 2)
		self.floor_y = floor_y

		# Declare virus state and select Sprites:
		self.state = self.create_state(force_bad)
		self.good_image = PhotoImage(file = f"Sprites/game_menu/virus/good_virus_1s.png")
		self.bad_image = PhotoImage(file = f"Sprites/game_menu/virus/{pick_from_list(['bad_virus_1s', 'bad_virus_2s'])}.png")

		# Spawn the virus and start the life state update cycle:
		self.spawn()
		self.life_state_update() # each 250ms

	def create_state(self, force_bad):
		''' Method to create the Virus state (good or bad)
			:inputs: force_bad (bool) if True, the virus is forced to be bad, otherwise randomized with 1/9 probability to be good '''
		if random_integer(1, 9) == 7 and not force_bad: # 1/9% probability
			return 'friendly'
		else:
			return 'unfriendly'

	def spawn(self):
		''' Method to spawn the Virus '''
		if self.state == 'friendly':
			self.character = self.canvas.create_image(self.x_pos, self.y_pos, image = self.good_image, anchor = "nw")
		else:
			self.character = self.canvas.create_image(self.x_pos, self.y_pos, image = self.bad_image, anchor = "nw")

	def update_position(self, game_speed):
		''' Method to constantly update the virus position
			:inputs: 'game_speed' (int) '''
		if not self.is_paused:
			speed_mult = 1 + ((200 - game_speed) / 50)
			if speed_mult < 0.3: speed_mult = 0.3
			# ---
			self.x_pos -= 7*speed_mult
			self.y_pos -= 7*self.angular*speed_mult
		self.canvas.coords(self.character, self.x_pos, self.y_pos)

	def life_state_update(self):
		''' Method to check if the virus is dead, if yes, destroys it '''
		if self.life == 'end' or (self.x_pos < -150) or (-100 > self.y_pos) or (self.y_pos > self.floor_y + 10):
			self.destroy()
		else:
			self.canvas.after(200, self.life_state_update)

	def destroy(self):
		''' Method to destroy the virus (and save calculations) '''
		self.destroyed = True
		self.life = 'end'
		self.canvas.delete(self.character)

	def pause(self):
		''' Method to pause/freeze the Virus '''
		self.is_paused = not self.is_paused



class Game_menu:
	''' :info: 	  A class used to create and launch a Game Party
		:inputs:  It takes as inputs: a frame (Frame) from where it is displayed
		:outputs: No returns from this class '''
	def __init__(self, frame):

		# Instances:
		self.frame = frame

	def create(self, main_menu, previous_frame):
		''' Method to initiate the Game Party 
		:inputs: 'main_menu' being the Play_menu canvas (Canvas), 'previous_frame' being the Play_menu's frame (Frame) ''' 
		# Sub-Instances:
		self.main_menu = main_menu
		self.previous_frame = previous_frame
		self.game_speed = 165 		# 1 = MAX, 200 = MIN
		self.all_virus = []
		self.floor_y = 850
		self.virus_limit = 2
		self.multiplier = 1
		self.green_count = 0 		# Count of green virus gotten
		self.maximum_complexity = 8 # Maximum nb of viruses to the screen	

	def open(self, name, mode):
		''' Method to open the Party 
		:inputs: 'name' being the current username of the player (str), 'mode' being the selected game mode (str) ''' 
		# Sub-Sub-Instances:
		self.frame.tkraise()
		self.name = name
		self.lost = False
		self.mode = mode
		self.is_paused = False

		# Canvas initialisation:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.focus_set()
		self.canvas.pack(fill = 'both', expand = True)

		# Background animation:
		self.background = Animated_Canvas(self.canvas, 0, 0, "Sprites/parallax/game_bg_0", 200)

		# Player and game mode initialisation:
		self.player = Player(self.canvas, self.floor_y)
		self.player.launch()
		if self.mode == 'lava': self.lava_mode_handler()
		self.player.create_cheat_texts()
		self.currently_slow, self.slowed_by = False, 0

		# Scoring elements initialisations:
		self.multiplier_time_bar = self.canvas.create_rectangle(1455, 75, 1455+450, 85, fill = '#fff', outline = '#fff')
		# --
		self.green_count_label = Updating_Label(self.canvas, 170, 70, f"{self.green_count}", "white", 40)
		self.green_count_label.add_image("Sprites/game_menu/other/virus_count")
		# --
		self.score_label = Updating_Label(self.canvas, 170, 930, f"{self.player.score}", 'white', 40)
		self.score_label.add_image("Sprites/game_menu/other/score_count")
		# --
		self.multiplier_label = Updating_Label(self.canvas, 1455, 50, f"Multiplier: x{self.multiplier}", 'white', 55)

		# Method and game updates initialisations:
		self.virus_display_update()
		self.virus_dead_update()
		self.virus_balls_colision()
		self.create_virus()
		self.game_speed_handler()
		self.virus_limit_handler()
		self.check_for_pause()
		self.check_for_boss_key()
		self.check_for_cheat()
		self.player_score_handler()
		self.player_arrival_animation()

		# Pause menu creation:
		self.pause_menu_image = PhotoImage(file = "Sprites/game_menu/other/pause_screen.png")
		self.pause_menu = self.canvas.create_image(0, 0, image = self.pause_menu_image, state = "hidden", anchor = "nw")
		self.pause_menu_state = False
		
		# Boss-key menu creation:
		self.boss_menu_image = PhotoImage(file = "Sprites/game_menu/other/boss_image.png")
		self.boss_menu = self.canvas.create_image(0, 0, image = self.boss_menu_image, state = "hidden", anchor = "nw")
		self.boss_menu_state = False

		# Pause-key binding and display:
		self.pause_key = self.player.keys['pause']
		if len(self.pause_key) <= 3: 
			self.pause_key_display = self.canvas.create_text(985, 398, text = f"' {self.pause_key.upper()} '", fill = "lightgrey", font = ("Helvetica Bold", 55), anchor = "nw", state = "hidden")
		else: 
			self.pause_key_display = self.canvas.create_text(985, 398, text = f"' {self.pause_key} '", fill = "lightgrey", font = ("Helvetica Bold", 55), anchor = "nw", state = "hidden")

	def check_for_pause(self):
		''' Method to check if the player has toggled the Pause menu '''
		if self.player.is_paused:
			self.player.pause()
			self.pause()
			for virus in self.all_virus:
				virus.pause()
			self.player.is_paused = False
			if not self.pause_menu_state:
				self.canvas.itemconfig(self.pause_menu, state = 'normal')
				self.canvas.itemconfig(self.pause_key_display, state = 'normal')
				self.canvas.tag_raise(self.pause_menu)
				self.canvas.tag_raise(self.pause_key_display)
				if self.boss_menu_state: self.canvas.tag_raise(self.boss_menu) # To be sure not to have collapsing when opening the BOSS menu
				self.pause_menu_state = True
			else: 
				self.canvas.itemconfig(self.pause_menu, state = 'hidden')
				self.canvas.itemconfig(self.pause_key_display, state = 'hidden')
				self.pause_menu_state = False

		if not self.lost: self.canvas.after(200, self.check_for_pause)

	def check_for_boss_key(self):
		''' Method to check if the player has toggled the Boss-key menu '''
		if self.player.boss_key_is_pressed:
			self.player.boss_key_is_pressed = False
			if not self.boss_menu_state:
				self.canvas.itemconfig(self.boss_menu, state = 'normal')
				self.canvas.tag_raise(self.boss_menu)
				if not self.pause_menu_state:
					self.player.is_paused = True
			else: 
				self.canvas.itemconfig(self.boss_menu, state = 'hidden')
			self.boss_menu_state = not self.boss_menu_state

		if not self.lost: self.canvas.after(300, self.check_for_boss_key)

	def check_for_cheat(self):
		''' Method to check if the player has toggled a cheat key '''
		if self.player.time_slow_activated and not self.currently_slow:
			self.slowed_by = (200-self.game_speed)//12
			self.game_speed *= self.slowed_by
			self.currently_slow = True
		if not self.player.time_slow_activated and self.currently_slow:
			self.game_speed //= self.slowed_by
			self.currently_slow = False

		if not self.lost: self.canvas.after(400, self.check_for_cheat)

	def lava_mode_handler(self, start_game = True):
		''' Method to create the animation of lava appeareance on screen 
			:inputs: No inputs should be passed/altered '''
		if start_game:
			self.lava_animation = Lava_Animation(self.canvas, self.floor_y)
			self.lava_animation.animate()
		if self.player.floor_colision() and self.player.score > 47 and not self.player.noclip_activated:
			self.lose()
		if not self.lost: self.canvas.after(200, lambda : self.lava_mode_handler(False))

	def player_arrival_animation(self):
		if self.player.x_pos < 555:
			self.player.x_pos += 20
			self.canvas.after(25, self.player_arrival_animation)

	def create_virus(self):
		''' Method to create a virus when conditions are met '''
		if len(self.all_virus) < self.virus_limit and not self.is_paused:
			if self.multiplier > 16: 
				new_virus = Virus(self.canvas, self.floor_y, True)
			else: 
				new_virus = Virus(self.canvas, self.floor_y)
			self.all_virus.append(new_virus)

		if not self.lost: self.canvas.after(self.game_speed*8+300, self.create_virus)

	def virus_display_update(self):
		''' Method to update virus display depending on its position '''
		if not self.is_paused and not self.lost:
			for virus in self.all_virus:
				virus.update_position(self.game_speed)
		if not self.lost: self.canvas.after(10, self.virus_display_update)

	def player_score_handler(self):
		''' Method to update the displayed player score '''
		if not self.is_paused:
			if self.player.time_slow_activated: 
				self.player.score += 1.35*self.multiplier*0.5
			else: 
				self.player.score += 1.35*self.multiplier
			self.score_label.update(f"{int(self.player.score)}")
		if not self.lost: self.canvas.after(200, self.player_score_handler)

	def virus_dead_update(self):
		''' Method to check if some viruses are dead '''
		if not self.is_paused: 
			self.all_virus = [virus for virus in self.all_virus if virus.life == 'alive']
		if not self.lost: self.canvas.after(200, self.virus_dead_update)

	def isColliding(self, virus):
		''' Method to check if a Virus collids with the Player
		:inputs: a virus (type:Virus)
		:outputs: Returns True if there is collision between the Virus and the Player '''
		if virus.x_pos + virus.width > self.player.x_pos and virus.x_pos < self.player.x_pos + self.player.width:
			if virus.y_pos + virus.height > self.player.y_pos and virus.y_pos < self.player.y_pos + self.player.height:
				return True
		return False

	def virus_balls_colision(self, time_since = 1000):
		''' Method to continiously check for all viruses collisions with the Player. If there is, call the methods to end the game
			:inputs: No inputs should be passed/altered '''
		if not self.is_paused:
			if time_since > 25000 - 500*self.multiplier: # If you didn't pick a green virus in the last 25s - 0.5s per multiplier, the multiplier resets
				self.multiplier = 1
				self.multiplier_label.update(f"Multiplier: x{self.multiplier}")
			for virus in self.all_virus:
				if self.isColliding(virus) and not self.player.noclip_activated:
					if virus.state == 'friendly':
						if time_since > 1000 and self.multiplier < 32:
							virus.destroy()
							self.multiplier *= 2
							self.green_count += 1
							self.multiplier_label.update(f"Multiplier: x{self.multiplier}")
							self.green_count_label.update(f"{self.green_count}")
							time_since = 0
					else : 
						self.lose()
						break
		self.canvas.coords(self.multiplier_time_bar, 1458, 120, 1458+300*self.multiplier_bar_update(time_since)+10, 130)
		if not self.lost : 
			if not self.is_paused: self.canvas.after(200, lambda : self.virus_balls_colision(time_since+200))
			else: self.canvas.after(200, lambda : self.virus_balls_colision(time_since))

	def multiplier_bar_update(self, time_since):
		''' Method to get the length of the multiplier bar depending on the actual multiplier and time since it has started
			:inputs: time_since (int) being the time since the multiplier bar has been filled
			:outputs: Returns the length (float) of the bar at the current time in the game '''
		if self.multiplier > 1:
			return 1 - (time_since / (25000 - 500*self.multiplier))
		else: return 0

	def game_speed_handler(self):
		''' Method to continiously update the game speed '''
		if not self.is_paused: 
			self.game_speed -= 1
		if self.game_speed > 1 and not self.lost: 
			self.canvas.after(3000, self.game_speed_handler)

	def virus_limit_handler(self):
		''' Method to increment the virus limit by 1 every 15s if it is not over the maximum limit '''
		if not self.is_paused: 
			self.virus_limit += 1
		if self.virus_limit <= self.maximum_complexity and not self.lost: 
			self.canvas.after(15000, self.virus_limit_handler)

	def save_game_to_leaderboard(self):
		''' Method to save the game scores to the leaderboard.txt external file '''
		leaderboard_file = open('leaderboard.txt', 'a')
		leaderboard_file.write(f"\n{int(self.player.score)} {self.name} {int(self.green_count)} {int(self.virus_limit)}")
		leaderboard_file.close()

	def lose(self):
		''' Method to display lose screen when dying and set the game state as 'lost' '''
		self.lost = True
		self.save_game_to_leaderboard()

		self.die_image = PhotoImage(file = "Sprites/game_menu/other/die_screen.png")
		self.die_screen = self.canvas.create_image(0, 0, image = self.die_image, anchor = "nw")
		self.die_score = self.canvas.create_text(1425, 335, text = f"{int(self.player.score)}", fill = "white", font = ("Helvetica Bold", 90), anchor = "n")
		self.press_key_label = self.canvas.create_text(840, 875, text = f"Press any key to leave", fill = "#c03939", font = ("Helvetica Bold", 45), anchor = "nw")
		self.canvas.after(400, lambda : self.canvas.bind("<KeyPress>", self.end_game))
	
	def end_game(self, event):
		''' Method to close the Game Party when lost '''
		self.canvas.after(300 - 200, lambda: self.main_menu.open())
		self.canvas.after(300 - 100, lambda: self.previous_frame.tkraise())
		self.canvas.after(300, lambda : self.canvas.destroy())

	def pause(self):
		''' Method to pause the Game '''
		self.is_paused = not self.is_paused




class Player:
	''' :info: 	  A class used to create a Player
		:inputs:  It takes as inputs: a canvas (Canvas) from where it is displayed, floor_y (int) as the y coordinates of the game floor
		:outputs: No returns from this class '''
	def __init__(self, canvas, floor_y):
		# Canvas initiation:
		self.canvas = canvas

		# Instances:
		self.floor_y = floor_y
		self.height, self.width = 150, 85
		self.x_pos, self.y_pos = -100, self.floor_y - self.height

		# Variables:
		self.keys = settings_read(0,5)
		self.is_paused = False
		self.boss_key_is_pressed = False
		self.noclip_activated = False
		self.time_slow_activated = False
		
	def launch(self):
		''' Method to launch the Player '''
		# Player animation:
		self.character = Animated_Canvas(self.canvas, self.x_pos, self.y_pos, "Sprites/game_menu/player/player_0", 6, 60)

		# Player attributes:
		self.flying = False
		self.score = 10

		# Player events:
		self.draw()
		self.gravity()
		self.moving_event()

		# player bindings:
		self.canvas.bind(f"<Key>", lambda event : self.key_handler(event, True))
		self.canvas.bind("<KeyRelease>", lambda event : self.key_handler(event, False))
		self.canvas.bind(f"<{self.keys['pause']}>", lambda event : self.pause(event))
		self.canvas.bind(f"<{self.keys['boss_key']}>", lambda event : self.boss_key_pressed(event))
		self.canvas.bind(f"<{self.keys['time_slow']}>", lambda event : self.time_slow_pressed(event))
		self.canvas.bind(f"<{self.keys['noclip']}>", lambda event : self.noclip_pressed(event))

	def floor_colision(self):
		''' Method to check if the Player is in collision with the floor '''
		if self.y_pos + self.height >= self.floor_y:
			return True
		return False

	def gravity(self):
		''' Method to apply gravity to the Player '''
		if not self.is_paused and not self.floor_colision():
			self.y_pos += 23
		self.canvas.after(15, self.gravity)

	def create_cheat_texts(self):
		''' Method to create and display cheat states when required '''
		self.noclip_cheat_text = self.canvas.create_text(950, 1010, text = "Noclip Cheat Activated", anchor = "n", state = "hidden", font = ("Helvetica Bold", 20))
		self.time_cheat_text = self.canvas.create_text(950, 1040, text = "Time Dilatation Cheat Activated", anchor = "n", state = "hidden", font = ("Helvetica Bold", 20))

	def key_handler(self, event, isPressed):
		''' Method to check for jump keypress
			:inputs: 'isPressed' (bool) which represents the state of the 'jump' key '''
		if event.keysym == self.keys['jump'] and isPressed:
			self.flying = True
		else: self.flying = False

	def moving_event(self):
		''' Method to continiously update/move the Character on jump-keypress, prevent from going over the roof, and change the Player sprites depending on its moving state '''
		if self.flying:
			self.y_pos -= 50
		if self.y_pos <= 100: self.y_pos = 100
		if self.y_pos >= self.floor_y-self.height:
			self.character.update_player_sprite('low')
		else: self.character.update_player_sprite('high')

		self.canvas.after(15, self.moving_event)

	def boss_key_pressed(self, event):
		''' Method to enable boss-keypress when associated key is pressed '''
		self.boss_key_is_pressed = not self.boss_key_is_pressed

	def time_slow_pressed(self, event):
		''' Method to enable time_slow when associated key is pressed '''
		if self.time_slow_activated:
			self.canvas.itemconfig(self.time_cheat_text, state = 'hidden')
		else:
			self.canvas.itemconfig(self.time_cheat_text, state = 'normal')
		self.time_slow_activated = not self.time_slow_activated

	def noclip_pressed(self, event):
		''' Method to enable noclip when associated key is pressed '''
		if self.noclip_activated:
			self.canvas.itemconfig(self.noclip_cheat_text, state = 'hidden')
		else:
			self.canvas.itemconfig(self.noclip_cheat_text, state = 'normal')
		self.noclip_activated = not self.noclip_activated

	def draw(self):
		''' Method to continiously draw the Player to the screen and update its position '''
		if not self.is_paused:
			self.canvas.coords(self.character.background, self.x_pos, self.y_pos)
		self.canvas.after(10, self.draw)

	def pause(self, event = None): 
		''' Method to pause the Player '''
		self.is_paused = not self.is_paused




