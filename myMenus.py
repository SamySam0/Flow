''' This file contains all the menus of our game '''
# ------------------------------------------------ #


# --- Module imports ---
from tkinter import *
from myAdds import *



# --- ALL MENUS ---

# - Primary Menus -

class Opening_menu:
	''' :info: 	  A class used to create and display the Opening menu
		:inputs:  It takes as inputs: the main root (type:root), frame (Frame) to where display the menu, next_frame (Frame)
		:outputs: No returns from this class '''
	def __init__(self, root, frame, next_frame):

		# Instances:
		self.frame = frame
		self.root = root
		self.next_frame = next_frame
		self.label_color = "white"

	def open(self):
		''' Method to open the menu (to save calculation when not in used) '''
		# Canvas initialisation:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.focus_set()
		self.canvas.bind("<Key>", lambda event : self.canvas.after(400, self.close))
		self.canvas.pack()

		# Background:
		self.background = PhotoImage(file = "Sprites/opening_menu/background.png")
		self.canvas.create_image(0, 0, image = self.background, anchor = 'nw')

		# Label animation:
		self.label = self.canvas.create_text(735, 715, text = "Press any button to start!", fill = self.label_color, font = ("Helvetica Bold", 32), anchor = "nw")
		self.label_animation()

	def label_animation(self):
		''' Method to animation the 'press to start' button '''
		if self.label_color == "grey":
			self.label_color = "white"
		else: self.label_color = "grey"
		self.canvas.itemconfig(self.label, fill = self.label_color)
		self.canvas.after(200, self.label_animation)

	def close(self):
		''' Method to call close_and_load function when press a key to start '''
		close_and_load(self.root, self.frame, self.next_frame, time = 3)



class Start_menu:
	''' :info: 	  A class used to create and display the Start menu
		:inputs:  It takes as inputs: the main root (type:root), frame (Frame) to where display the menu, next_menus (Canvas)
		:outputs: No returns from this class '''
	def __init__(self, root, frame, next_menus):

		# Instances:
		self.frame = frame
		self.root = root
		self.next_menus = next_menus

	def open(self):
		''' Method to open the menu (to save calculation when not in used) '''
		# Canvas initialisation:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_main/main_bg", 159)

		# Create and display Buttons:
		Image_Button(self.canvas, 1020, 200, "Sprites/main_menu/Buttons/play_off.png", "Sprites/main_menu/Buttons/play_on.png", self.play)
		Image_Button(self.canvas, 1035, 482, "Sprites/main_menu/Buttons/settings_off.png", "Sprites/main_menu/Buttons/settings_on.png", self.settings)
		Image_Button(self.canvas, 1070, 758, "Sprites/main_menu/Buttons/extra_off.png", "Sprites/main_menu/Buttons/extra_on.png", self.extras)
		Image_Button(self.canvas, 1470, 748, "Sprites/main_menu/Buttons/quit_off.png", "Sprites/main_menu/Buttons/quit_on.png", self.quit)

	def play(self):
		''' Method to move to Play menu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['play'].open(self))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def settings(self):
		''' Method to move to Settings menu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['settings'].open(self))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def extras(self):
		''' Method to move to Extras menu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['extras'].open(self))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def quit(self):
		''' Method to quit the game '''
		self.root.quit()




# - In-menu Menus -

class Extras_menu:
	''' :info: 	  A class used to create and display the Extras menu
		:inputs:  It takes as inputs: the main root (type:root), frame (Frame) to where display the menu, next_menus (Canvas)
		:outputs: No returns from this class '''
	def __init__(self, frame):

		# Instances:
		self.frame = frame

	def open(self, previous_menu):
		''' Method to open the menu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.focus_set()
		self.canvas.bind("<Escape>", lambda event: self.back(event))
		self.canvas.pack(fill = 'both', expand = True)

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_menu/menu_0", 150)

		# "< Back" buttons:
		Image_Button(self.canvas, 80, 45, "Sprites/main_menu/Buttons/back_off.png", "Sprites/main_menu/Buttons/back_on.png", self.back)

		# Create and display Information blocks:
		self.boss_key_image = PhotoImage(file = "Sprites/main_menu/extras/boss_key.png")
		self.information_block(100, 205, "Boss Key", f"Hey man, Firebol here! Be careful behind you, I can see your Boss keeps moving around. Let me help you; you have set your Boss key to '{settings_read()['boss_key'].upper()}'! Press it as fast as you can if your Boss comes in. I have to leave now, my wice is waiting me for dinner!", self.boss_key_image)

		self.time_image = PhotoImage(file = "Sprites/main_menu/extras/clock.png")
		self.information_block(100*2 + (1920-300)/2, 205, "Time Retraction Cheat", f"Time Retraction is THE cheat everyone would like to get in real life. You want to run between bullets, and go faster than your problems? Then you might want to slow down TIME. By pressing your '{settings_read()['time_slow'].upper()}' key, the time will slow down. But your reflexes won't. Oh, and we might also give you a small break at this point.", self.time_image)

		self.noclip_image = PhotoImage(file = "Sprites/main_menu/extras/noclip.png")
		self.information_block(100, 555, "Noclip Cheat", f"You see that wall behind your computer? Maybe your kitchen is behind it, and you might want to grab a beer from your fridge. Well, what if you could fly straight thourgh the wall? This is the NOCLIP. By pressing your '{settings_read()['noclip'].upper()}' key, you will be able to fly through any obstacle. IN THE GAME!! Don't try this with your Kitchen!", self.noclip_image)

		self.lava_image = PhotoImage(file = "Sprites/main_menu/extras/lava.png")
		self.information_block(100*2 + (1920-300)/2, 555, "The Floor is Lava Mode", "If by any chance you find the game too easy, because you have 3 hands for example; You will be able to choose our custome mode before launching. Specially for you, we added a \"Floor is Lava Mode\". It is pretty simple. FLY, FLY, FLY AND NEVER GO DOWN! If you touch the floor... you DIE! Annoying hein?", self.lava_image)


	def back(self, event = None):
		''' Method to move back to Start menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open())
		self.canvas.after(300, lambda : self.canvas.destroy())

	def information_block(self, x_pos, y_pos, title, text, image):
		''' Method to create and display an information block '''
		Boxed_Label(self.frame, self.canvas, x_pos, y_pos, title, "darkred", "white", 27, (1920-300)/2) #Window size - 3*spaces / nb_of_blocks
		self.canvas.create_image(x_pos, y_pos + 50, image = image, anchor = "nw")
		self.canvas.create_text(x_pos + 255, y_pos + 65, text = text, fill = "white", width = 550, font = ("Courier", 22), anchor = "nw")



class Play_menu:
	''' :info: 	  A class used to create and display the Play menu
		:inputs:  It takes as inputs: the frame (Frame) to where display the menu, next_menus (Canvas)
		:outputs: No returns from this class '''
	def __init__(self, frame, next_menu):
		# Instances:
		self.frame = frame
		self.next_menu = next_menu

	def open(self, previous_menu):
		''' Method to open the menu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu
		self.player_name = self.get_username()

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)
		self.canvas.focus_set()
		self.canvas.bind("<Escape>", lambda event: self.back(event))

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_menu/menu_0", 150)

		# "< Back" Button:
		Image_Button(self.canvas, 80, 45, "Sprites/main_menu/Buttons/back_off.png", "Sprites/main_menu/Buttons/back_on.png", self.back)

		# - Create and display "Set name" Button: -
		# Image:
		self.nametag_image = PhotoImage(file = "Sprites/main_menu/play_menu/name_tag.png")
		self.canvas.create_image(1200, 950, image = self.nametag_image)
		# Name Entry:
		self.entry = Entry(self.canvas, bg = 'white', width = 32, relief = 'flat', font = ("Helvetica", 25), fg = 'grey', selectforeground = 'darkgrey', bd=0, highlightthickness=0)
		self.entry.place(x = 1015, y = 880, height = 80)
		# Save Button:
		self.save_button = Save_Button(self.frame, self.canvas, 1650, 920, 'darkred', True)
		self.canvas.create_text(1080, 860, text = "Enter your name:", fill = 'white', font = ("Helvetica", 20))
		# Save Button bindings:
		self.save_button.canvas.tag_bind(self.save_button.image, "<Button-1>", lambda event : self.save_name(self.entry, self.save_button, event))
		self.save_button.canvas.tag_bind(self.save_button.title, "<Button-1>", lambda event : self.save_name(self.entry, self.save_button, event))

		# Create and display Leaderboard Background:
		self.leaderboard_image = PhotoImage(file = "Sprites/main_menu/play_menu/leaderboard.png")
		self.canvas.create_image(1375, 445, image = self.leaderboard_image)
		# Create and display "Reset Leaderboard" Button:
		self.reset_leaderboard = self.canvas.create_text(1768, 163, text = "Reset", font = ("Helvetica Bold", 25))
		self.canvas.tag_bind(self.reset_leaderboard, "<Button-1>", lambda event : self.leaderboard_reset(event))
		# Display Leaderboard:
		self.pack = []
		self.display_leaderboard()
		
		# Create and siplay "Game Modes" Menu:
		self.game_mode = Mode_Menu(self.canvas, 260, 550)

		# Create, display and bind "Play" Button:
		self.play_button_image = PhotoImage(file = "Sprites/main_menu/play_menu/PLAY.png")
		self.play_button = self.canvas.create_image(440, 925, image = self.play_button_image)
		self.canvas.tag_bind(self.play_button, "<Button-1>", lambda event : self.play(event))

		# Title/Indications for "Game Mode" Menu:
		self.canvas.create_text(454, 200, text = "Click to select your game mode:", font = ("Helvetica Bold", 48), fill = "white")

	def get_username(self):
		''' Method to get the current username of the player
			:outputs: Returns the current username '''
		name_file = open("username.txt", "r")
		player_name = name_file.readline()
		name_file.close()
		return player_name

	def change_username(self, new_username):
		''' Method to write a new username to external username.txt file
			:inputs: 'new_name' (str) '''
		name_file = open("username.txt", "w")
		if len(new_username) < 1: new_username = "Unknown"
		name_file.write(new_username)
		name_file.close()

	def play(self, event):
		''' Method to launch a game with the selected game mode '''
		mode = self.game_mode.get_mode()
		self.canvas.after(300 - 200, lambda: self.next_menu.create(self.previous_menu, self.frame))
		self.canvas.after(300 - 100, lambda: self.next_menu.open(self.player_name, mode))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def save_name(self, entry, save_button, event):
		''' Method to make the "Save" button responsive
			:inputs: 'entry' (Entry:Object), 'save_button' (Button) '''
		if save_button.text == 'Save':
			save_button.text = 'Saved!'
		save_button.canvas.itemconfig(save_button.title, text = save_button.text)
		save_button.canvas.after(1000, lambda : self.saved(save_button))

		name = entry.get().replace(' ', '')[:15]
		self.change_username(name)
		self.player_name = self.get_username()

	def saved(self, save_button):
		''' Method to display 'Save' when the new username has been saved
			:inputs: 'save_button' (Button) '''
		save_button.text = 'Save'
		save_button.canvas.itemconfig(save_button.title, text = save_button.text)

	def back(self, event = None):
		''' Method to move back to Start menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open())
		self.canvas.after(300, lambda : self.canvas.destroy())

	def display_leaderboard(self):
		''' Method to create and display the Leaderboard '''
		self.leaderboard_capacity, self.height = 6, 375
		self.scores = leaderboard_read()
		self.scores = sorted(self.scores)[::-1]
		for score in self.scores[:self.leaderboard_capacity]:
			self.score = score[0]
			self.username = score[1]
			self.green_gotten = score[2]
			self.aggressivity = score[3]
			self.line = Leaderboard_Line(self.canvas, 958, self.height, self.username, self.score, self.green_gotten, self.aggressivity)
			self.pack.append(self.line)
			self.height += 70

	def leaderboard_reset(self, event):
		''' Method to reset the Leaderboard (excluding Creator score) '''
		file = open("leaderboard.txt", "w")
		file.truncate(0)
		file.write("37162 Creator 28 12")
		file.close()
		for line in self.pack:
			line.clear_line()
		self.pack = []
		self.display_leaderboard()



class Settings_menu:
	''' :info: 	  A class used to create and display the Settings menu
		:inputs:  It takes as inputs: the frame (Frame) to where display the menu, next_menus (Canvas)
		:outputs: No returns from this class '''
	def __init__(self, frame, next_menus):
		# Instances:
		self.frame = frame
		self.next_menus = next_menus

	def open(self, previous_menu):
		''' Method to open the menu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)
		self.canvas.focus_set()
		self.canvas.bind("<Escape>", lambda event: self.back(event))

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/settings_menu/bg_animation/settings_bg_0", 250)

		# "< Back" Button:
		Image_Button(self.canvas, 80, 45, "Sprites/main_menu/Buttons/back_off.png", "Sprites/main_menu/Buttons/back_on.png", self.back)

		# Create, display and link Sub-Menu Buttons:
		Image_Button(self.canvas, 165, 765, "Sprites/main_menu/Buttons/sound_off.png", "Sprites/main_menu/Buttons/sound_on.png", self.sound)
		Image_Button(self.canvas, 1100, 205, "Sprites/main_menu/Buttons/controls_off.png", "Sprites/main_menu/Buttons/controls_on.png", self.controls)
		Image_Button(self.canvas, 525, 445, "Sprites/main_menu/Buttons/video_off.png", "Sprites/main_menu/Buttons/video_on.png", self.video)
		
	def back(self, event = None):
		''' Method to move Back to Start menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open())
		self.canvas.after(300, lambda : self.canvas.destroy())

	def video(self):
		''' Method to move to Video SubMenu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['video'].open(self, self.previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def sound(self):
		''' Method to move to Sound SubMenu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['sound'].open(self, self.previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())

	def controls(self):
		''' Method to move to Controls SubMenu '''
		self.canvas.after(300 - 200, lambda: self.next_menus['controls'].open(self, self.previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())




# - Settings SubMenus -

class Video_menu:
	''' :info: 	  A class used to create and display the Settings-Video SubMenu
		:inputs:  It takes as inputs: the frame (Frame) to where display the menu
		:outputs: No returns from this class '''
	def __init__(self, frame):
		# Instances:
		self.frame = frame

	def open(self, previous_menu, previous_previous_menu):
		''' Method to open the SubMenu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas), 'previous_previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu
		self.previous_previous_menu = previous_previous_menu

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)
		self.canvas.focus_set()
		self.canvas.bind("<Escape>", lambda event: self.back(event))

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_menu/menu_0", 150)
		self.wheel_background_image = PhotoImage(file = "Sprites/main_menu/settings_menu/video_hover.png")
		self.canvas.create_image(0, 0, image = self.wheel_background_image, anchor = "nw")

		# "< Done" Button:
		Image_Button(self.canvas, 1575, 45, "Sprites/main_menu/Buttons/done_off.png", "Sprites/main_menu/Buttons/done_on.png", self.back)

		# - Create and Display Buttons/Selectors for each Settings: -
		# Selectors:
		Selector(self.frame, self.canvas, 785, 300, "darkred", "Fullscreen", "fullscreen")
		Selector(self.frame, self.canvas, 785, 620, "darkred", "V-Sync", "v_sync")
		# Save Button:
		Save_Button(self.frame, self.canvas, 935, 860, "darkred")

	def back(self, event = None):
		''' Method to move Back to Settings menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open(self.previous_previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())



class Sound_menu:
	''' :info: 	  A class used to create and display the Sound Settings-SubMenu
		:inputs:  It takes as inputs: the frame (Frame) to where display the menu
		:outputs: No returns from this class '''
	def __init__(self, frame):
		# Instances:
		self.frame = frame

	def open(self, previous_menu, previous_previous_menu):
		''' Method to open the SubMenu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas), 'previous_previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu
		self.previous_previous_menu = previous_previous_menu

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)
		self.canvas.focus_set()
		self.canvas.bind("<Escape>", lambda event: self.back(event))

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_menu/menu_0", 150)
		self.wheel_background_image = PhotoImage(file = "Sprites/main_menu/settings_menu/sound_hover.png")
		self.canvas.create_image(0, 0, image = self.wheel_background_image, anchor = "nw")

		# "< Done" Button:
		Image_Button(self.canvas, 1575, 45, "Sprites/main_menu/Buttons/done_off.png", "Sprites/main_menu/Buttons/done_on.png", self.back)

		# - Create and Display Buttons/Selectors for each Settings: -
		# Selectors:
		Selector(self.frame, self.canvas, 785, 300, "darkred", "Music", "music")
		Selector(self.frame, self.canvas, 785, 620, "darkred", "Sounds", "sound")
		# Save Button:
		Save_Button(self.frame, self.canvas, 935, 860, "darkred")

	def back(self, event = None):
		''' Method to move Back to Settings menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open(self.previous_previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())



class Controls_menu:
	''' :info: 	  A class used to create and display the Controls Settings-SubMenu
		:inputs:  It takes as inputs: the frame (Frame) to where display the menu
		:outputs: No returns from this class '''
	def __init__(self, frame):
		# Instances:
		self.frame = frame

	def open(self, previous_menu, previous_previous_menu):
		''' Method to open the SubMenu (to save calculation when not in used) 
			:inputs: Takes as inputs: 'previous_menu' (Canvas), 'previous_previous_menu' (Canvas) '''
		# Sub-Local Instances:
		self.previous_menu = previous_menu
		self.previous_previous_menu = previous_previous_menu

		# Canvas initialisation and bindings:
		self.canvas = Canvas(self.frame, width = 1920, height = 1080, highlightthickness = 0)
		self.canvas.pack(fill = 'both', expand = True)

		# Background animation:
		Animated_Canvas(self.canvas, 0, 0, "Sprites/main_menu/bg_menu/menu_0", 150)
		self.wheel_background_image = PhotoImage(file = "Sprites/main_menu/settings_menu/controls_hover.png")
		self.canvas.create_image(0, 0, image = self.wheel_background_image, anchor = "nw")

		# "< Done" Button:
		Image_Button(self.canvas, 1575, 45, "Sprites/main_menu/Buttons/done_off.png", "Sprites/main_menu/Buttons/done_on.png", self.back)

		# - Create and Display Buttons/Key-Selectors for each Settings: -
		# Key Selectors:
		Key_Selector(self.frame, self.canvas, 635, 340, "darkred", "Jump", "jump", False)
		Key_Selector(self.frame, self.canvas, 575, 670, "darkred", "NoClip", "noclip")
		Key_Selector(self.frame, self.canvas, 635 + 415, 340, "darkred", "Pause", "pause")
		Key_Selector(self.frame, self.canvas, 575 + 415, 670, "darkred", "Time Slow", "time_slow")
		Key_Selector(self.frame, self.canvas, 575 + 415 + 425, 505, "darkred", "Boss Key", "boss_key")
		# Save Button:
		Save_Button(self.frame, self.canvas, 935, 925, "darkred")

	def back(self, event = None):
		''' Method to move Back to Settings menu '''
		self.canvas.after(300 - 200, lambda: self.previous_menu.open(self.previous_previous_menu))
		self.canvas.after(300, lambda : self.canvas.destroy())




