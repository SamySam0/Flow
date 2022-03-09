''' This file contains all the global functions and classes for our game '''
# ------------------------------------------------------------------------ #


# --- Module imports ---
from tkinter import *



# --- Main Classes ---

class Image_Button :
	''' :info: 	  A class used to create and display buttons, with hover animation, and which calls a bind-action when clicked
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), x_pos (int), y_pos (int), the folder of 'image_directory' (str), hover_image_directory: the one of it's hover image (str), action (function) by default: None
		:outputs: No returns from this class '''
	def __init__(self, canvas, x_pos, y_pos, image_directory, hover_image_directory, action = None):

		# Instances:
		self.canvas = canvas
		self.button_image = PhotoImage(file = image_directory)
		self.hover_button_image = PhotoImage(file = hover_image_directory)

		# Create and display Button:
		self.button = canvas.create_image(x_pos, y_pos, image = self.button_image, anchor = "nw")

		# Button bindings:
		self.canvas.tag_bind(self.button, "<Enter>", self.hover)
		self.canvas.tag_bind(self.button, "<Leave>", self.not_hover)
		self.canvas.tag_bind(self.button, "<Button-1>", lambda event : action())

	def hover(self, event):
		''' Event Method to change the image when mouse is hover the button '''
		self.canvas.itemconfig(self.button, image = self.hover_button_image)

	def not_hover(self, event):
		''' Event Method to change the image when mouse leaves the button '''
		self.canvas.itemconfig(self.button, image = self.button_image)



class Updating_Label :
	''' :info: 	  A class used to create and display texts which can be changed/updated with update() method
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), x_pos (int), y_pos (int), the 'text' (str), font_size (int), font_family (str) by default: "Helvetica Bold"
		:outputs: No returns from this class '''
	def __init__(self, canvas, x_pos, y_pos, text, text_color, font_size, font_family = "Helvetica Bold"):
		
		# Instances:
		self.canvas = canvas
		self.x_pos, self.y_pos = x_pos, y_pos

		# Create and display Label:
		self.label = self.canvas.create_text(x_pos, y_pos, text = text, fill = text_color, font = (font_family, font_size), anchor = "nw")

	def update(self, text):
		''' Method to update displayed text when called 
			:inputs: text (str) '''
		self.canvas.itemconfig(self.label, text = text)

	def add_image(self, image):
		''' Method to add an image on the left of the text
			:inputs: complete path of the image (without its extension) '''
		self.new_image = PhotoImage(file = f"{image}.png")
		self.canvas.create_image(self.x_pos - 105, self.y_pos - 20, image = self.new_image, anchor = "nw")



class Boxed_Label :
	''' :info: 	  A class used to create and display a boxed text
		:inputs:  It takes as inputs: a window (root), a canvas where to display (type:Canvas), x_pos (int), y_pos (int), the 'text' (str), 'text_color' (str), 'background_color' (str), font_size (int), width (int) by default: "None", height (int) by default : "None", font_family (str) by default: "Helvetica Bold"
		:outputs: No returns from this class '''
	def __init__(self, window, canvas, x_pos, y_pos, text, text_color, background_color, font_size, width = None, height = None, font_family = "Helvetica Bold"):

		# - Create and display Boxed Label: -
		# Label:
		self.label = Label(window, text = text, fg = text_color, bg = background_color, font = (font_family, font_size))
		# Box:
		self.boxed_Label = canvas.create_window(x_pos, y_pos, width = width, height = height, anchor = "nw", window = self.label)



class Animated_Canvas:
	''' :info: 	  A class used to create and display an animated picture to be used as a background
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), x_pos (int), y_pos (int), complete path of 'image_name' (without its extension) (str), 'frame_amount': number of frames (int), 'display_rate': frame rate (int)
		:outputs: No returns from this class '''
	def __init__(self, canvas, x_pos, y_pos, image_name, frame_amount, display_rate = 25):

		# Instances:
		self.canvas = canvas
		self.display_rate = display_rate 	# in ms
		self.default_image = image_name
		self.image_name = image_name
		self.frame_amount = frame_amount
		self.frame_count = 1

		# Initiate First image:
		self.first_image = PhotoImage(file = f"{self.image_name}1.png")
		# Display First Image:
		self.background = self.canvas.create_image(0, 0, image = self.first_image, anchor = "nw")

		# Launch animation:
		self.animate()

	def animate(self):
		''' Method to display image frames as an animation '''
		self.next_image = PhotoImage(file = f"{self.next_frame()}.png")
		self.canvas.itemconfig(self.background, image = self.next_image)
		self.canvas.after(self.display_rate, self.animate)

	def next_frame(self):
		''' Method to determine the next image in the animation
			:outputs: Returns the complete path (without extesnion) of the next image on the animation '''
		self.frame_count = self.frame_count%self.frame_amount + 1
		return f"{self.image_name}{self.frame_count}"

	def update_player_sprite(self, state):
		''' Method to animate the player sprite (ONLY!) 
			:inputs: current state of the player (str: "high" or "low") '''
		if self.image_name == self.default_image and state == 'high':
			self.image_name = "Sprites/game_menu/player/flight_0"
		else: 
			if state == 'low': self.image_name = self.default_image



class Selector: 
	''' :info: 	  A class used to create and display a 'ON'/'OFF' settings selector linked with the external settings file
		:inputs:  It takes as inputs: a window (root), a canvas where to display (type:Canvas), x_pos (int), y_pos (int), 'text_color' (str), setting 'title' (str), 'setting_name' from setting's file (str)
		:outputs: No returns from this class '''
	def __init__(self, window, canvas, x_pos, y_pos, text_color, title, setting_name):

		# - Instances: -
		# Setting Initiation Linked with Global "settings.txt":
		if settings_read()[setting_name] == 'True': self.text = 'ON'
		else: self.text = 'OFF'
		# Variables:
		self.window = window
		self.canvas = canvas
		self.setting_name = setting_name
		self.title = title

		# Create and display Background:
		self.background = PhotoImage(file = "Sprites/main_menu/settings_menu/selector_bg.png")
		self.image = self.canvas.create_image(x_pos + 147, y_pos - 22, image = self.background)

		# Create and display Left Arrow:
		self.left_arrow = self.canvas.create_text(x_pos, y_pos, text = "<", fill = text_color, font = ("Helvetica Bold", 60), anchor = "nw")
		self.canvas.tag_bind(self.left_arrow, "<Button-1>", self.action)

		# Create and display Middle Lable:
		self.label = self.canvas.create_text(x_pos + 150, y_pos + 5, text = self.text, width = 135, fill = text_color, font = ("Helvetica Bold", 60), anchor = "n")

		# Create and Display Right Arrow:
		self.right_arrow = self.canvas.create_text(x_pos + 260, y_pos, text = ">", fill = text_color, font = ("Helvetica Bold", 60), anchor = "nw")
		self.canvas.tag_bind(self.right_arrow, "<Button-1>", self.action)

		# Create and display Title:
		self.title_text = canvas.create_text(x_pos + 155, y_pos - 132, text = self.title, fill = text_color, font = ("Helvetica Bold", 50), anchor = "n")

	def action(self, event):
		''' Method to take action and link the selected settings with the external settings file '''
		if self.text == 'ON':
			self.text = 'OFF'
			settings_write(self.setting_name, 'False')
		else: 
			self.text = 'ON'
			settings_write(self.setting_name, 'True')

		# Apply fullscreen settings and update current fullscreen state:
		if self.title == 'Fullscreen':
			self.window._nametowidget('.').attributes('-fullscreen', settings_read()['fullscreen'])
			self.window._nametowidget('.').geometry("1920x1080")

		# Update displayed state text:
		self.canvas.itemconfig(self.label, text = self.text)



class Key_Selector:
	''' :info: 	  A class used to create and display a key selector linked with the external settings file
		:inputs:  It takes as inputs: a window (root), a canvas where to display (type:Canvas), x_pos (int), y_pos (int), 'text_color' (str), setting 'title' (str), 'key_name' of the key from setting's file (str), 'enable' (bool) determines if the key_selector is enable - default: True
		:outputs: No returns from this class '''
	def __init__(self, window, canvas, x_pos, y_pos, text_color, title, key_name, enable = True):

		# - Instances: -
		# Displayed text link with Global "settings.txt":
		self.text = settings_read(0, 9)[key_name].upper()
		if self.text == 'UP': self.text = '^' # To make sure
		if self.text == 'ESCAPE': self.text = 'ESC'
		# Variables:
		self.key_name = key_name
		# Canvas:
		self.canvas = canvas
		self.canvas.focus_set()

		# Create, display and bind Menu's Image:
		self.image = PhotoImage(file = "Sprites/main_menu/settings_menu/key_bg.png")
		self.menu_background = self.canvas.create_image(x_pos + 2, y_pos, image = self.image, anchor = "center")
		self.canvas.tag_bind(self.menu_background, "<Button-1>", lambda event : self.action(enable, event))

		# Create and display Key Title:
		self.title = canvas.create_text(x_pos, y_pos - 112, text = title, fill = text_color, font = ("Helvetica Bold", 50), anchor = "n")

		# Create, display and bind Key Name (as text):
		self.key_text = self.canvas.create_text(x_pos, y_pos + 34, text = self.text, fill = 'black', font = ("Helvetica Bold", 50), anchor = "n")
		if enable: self.canvas.tag_bind(self.key_text, "<Button-1>", lambda event : self.action(enable, event))

	def action(self, enable, event):
		''' Method to take action and link the selected key with the external key settings file 
			:inputs: 'enable' (bool) to only perform the binding action if True '''
		if not enable: return
		self.change_key_image = PhotoImage(file = "Sprites/main_menu/settings_menu/new_key.png")
		self.change_key_menu = self.canvas.create_image(0, 0, image = self.change_key_image, anchor = "nw")
		self.canvas.bind("<KeyPress>", lambda event : self.record_key(self.change_key_menu, event))

	def record_key(self, change_key_menu, event):
		''' Method to record the key when performing setting edit 
			:inputs: "change_key_menu" (Canvas) '''
		settings_write(self.key_name, event.keysym)
		self.canvas.unbind("<KeyPress>")
		self.text = settings_read(0, 9)[self.key_name].upper()
		if self.text == 'UP': self.text = '^'
		if self.text == 'ESCAPE': self.text = 'ESC'
		self.canvas.itemconfig(self.key_text, text = self.text)
		self.canvas.delete(change_key_menu)



class Save_Button:
	''' :info: 	  A class used to create and display a "Save" button
		:inputs:  It takes as inputs: a window (root), a canvas where to display (type:Canvas), x_pos (int), y_pos (int), 'text_color' (str), setting 'title' (str), 'key_name' of the key from setting's file (str), 'name_save' by default: False -> if True save player's 'username' to settings
		:outputs: No returns from this class '''
	def __init__(self, window, canvas, x_pos, y_pos, text_color, name_save = False):

		# Instances:
		self.text = 'Save'
		self.canvas = canvas

		# Create, display and bind Button:
		if name_save != 'False': self.to_use = PhotoImage(file = "Sprites/main_menu/play_menu/name_save.png")
		else: self.to_use = PhotoImage(file = "Sprites/main_menu/settings_menu/btn.png")
		self.image = self.canvas.create_image(x_pos, y_pos, image = self.to_use)
		self.canvas.tag_bind(self.image, "<Button-1>", self.save)

		# Create, display and bind Title:
		# We also bind the Title so if the player clicks on the button OR the Title, it will toggle Save Function for both cases
		self.title = canvas.create_text(x_pos, y_pos - 20, text = self.text, fill = text_color, font = ("Helvetica Bold", 35), anchor = "n")
		self.canvas.tag_bind(self.title, "<Button-1>", self.save)

	def save(self, event):
		''' Method to Save settings and display "Saved!" state '''
		if self.text == 'Save':
			self.text = 'Saved!'
		self.canvas.itemconfig(self.title, text = self.text)
		self.canvas.after(1000, self.saved)

	def saved(self):
		''' Method to end displaying "Saved!" state '''
		self.text = 'Save'
		self.canvas.itemconfig(self.title, text = self.text)



class Leaderboard_Line:
	''' :info: 	  A class used to create and display a single line of the leaderboard
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), x_pos (int), y_pos (int); game stats: 'username' (str), 'score' (int/str), 'green_gotten' (int/str), 'aggressivity' (int/str)
		:outputs: No returns from this class '''
	def __init__(self, canvas, x_pos, y_pos, username, score, green_gotten, aggressivity):

		# Instances:
		self.canvas = canvas

		# Create and display each score attributes:
		self.username_line = self.canvas.create_text(x_pos + 182 + 70, y_pos, width = None, text = username, fill = 'black', font = ("Helvetica Bold", 30), anchor = "n", tag = "line")
		self.score_line = self.canvas.create_text(x_pos + 40, y_pos, width = None, text = f"{score}", fill = 'black', font = ("Helvetica Bold", 30), anchor = "n", tag = "line")
		self.green_gotten_line = self.canvas.create_text(x_pos + 182 + 297, y_pos, width = None, text = f"{green_gotten}", fill = 'black', font = ("Helvetica Bold", 30), anchor = "n", tag = "line")
		self.agressivity_line = self.canvas.create_text(x_pos + 182 + 297 + 250, y_pos, width = None, text = f"{aggressivity}", fill = 'black', font = ("Helvetica Bold", 30), anchor = "n", tag = "line")

	def clear_line(self):
		''' Method to delete a line '''
		self.canvas.delete("line")



class Mode_Menu :
	''' :info: 	  A class used to create and display the "chose game mode" Menu
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), x_pos (int), y_pos (int)
		:outputs: No returns from this class '''
	def __init__(self, canvas, x_pos, y_pos):

		# Instances:
		self.canvas = canvas
		self.game_mode = 'normal'

		# Create and display Game Mode Menus:
		self.normal_image = PhotoImage(file = "Sprites/main_menu/play_menu/normal.png")
		self.normal_image_disabled = PhotoImage(file = "Sprites/main_menu/play_menu/normal_bw.png")
		self.lava_image = PhotoImage(file = "Sprites/main_menu/play_menu/lava.png")
		self.lava_image_disabled = PhotoImage(file = "Sprites/main_menu/play_menu/lava_bw.png")

		# Bind "button" function to Game Mode Menus:
		self.normal_current_image = self.normal_image
		self.normal_button = self.canvas.create_image(x_pos, y_pos, image = self.normal_current_image)
		self.lava_current_image = self.lava_image_disabled
		self.lava_button = self.canvas.create_image(x_pos + 400, y_pos, image = self.lava_current_image)

		# Button bindings:
		self.canvas.tag_bind(self.normal_button, "<Button-1>", lambda event : self.click('normal'))
		self.canvas.tag_bind(self.lava_button, "<Button-1>", lambda event : self.click('lava'))

	def click(self, from_button):
		''' Method as response to Game_mode menu selector's click/selection
			:inputs: "from_button"'s name from which the selector was clicked ("normal" or "lava") '''
		if from_button == 'normal':
			if self.normal_current_image != self.normal_image:
				self.normal_current_image = self.normal_image
				self.lava_current_image = self.lava_image_disabled
				self.game_mode = 'normal'
		else:
			if self.lava_current_image != self.lava_image:
				self.lava_current_image = self.lava_image
				self.normal_current_image = self.normal_image_disabled
				self.game_mode = 'lava'

		# Update menu's images after mode set:
		self.canvas.itemconfig(self.normal_button, image = self.normal_current_image)
		self.canvas.itemconfig(self.lava_button, image = self.lava_current_image)

	def get_mode(self):
		''' Returns the currently selected game mode '''
		return self.game_mode



class Lava_Animation:
	''' :info: 	  A class used to create and display the lava animation at game launch when "lava" game mode is selected
		:inputs:  It takes as inputs: a canvas where to display (type:Canvas), floor_y (int) being y coordinates of the floor
		:outputs: No returns from this class '''
	def __init__(self, canvas, floor_y):

		# Instances:
		self.canvas = canvas
		self.floor_y = floor_y
		self.lava_y_pos = 1085

		# Lava Image initiation:
		self.lava_image = PhotoImage(file = "Sprites/game_menu/other/lava_floor.png")
		self.lava = self.canvas.create_image(0, self.lava_y_pos, image = self.lava_image, anchor = "nw")

	def animate(self):
		''' Method to launch lava appearance animation '''
		if self.lava_y_pos > self.floor_y-12:
			self.lava_y_pos -= 3
			self.canvas.move(self.lava, 0, -3)
			self.canvas.after(50, self.animate)




# --- Main Functions ---

def close_and_load(root, frame_to_close, frame_to_open, time):
	''' :info: 	  A function used as a transaction between two frames, and displaying the waiting screen during process
		:inputs:  It takes as inputs: the main root (root), name of "frame_to_close" (Frame), name of "frame_to_open" (Frame), waiting screen display "time" (int) in ms
		:outputs: No returns from this class '''

	# Local variables :
	ONE_SECOND_IN_MS, TIME_HANDLE = 1000, 200
	# Create waiting_screen's Frame
	waiting_frame = Frame(root, width = 1920, height = 1080)
	waiting_frame.grid(row=0, column=0)
	# Create waiting_screen's Canvas
	waiting_screen = Canvas(waiting_frame, width = 1920, height = 1080, highlightthickness = 0)
	waiting_screen.pack(fill = 'both', expand = True)
	# Create waiting_screen animation
	Animated_Canvas(waiting_screen, 0, 0, "Sprites/loading_screen/LOADING", 4, 150)
	# When finished setting-up, raise it on screen
	waiting_frame.tkraise()
	# Then destroy the Frame to close
	frame_to_close.destroy()
	# After <time> seconds, open the next frame and destroy the waiting_screen's Frame
	waiting_screen.after(ONE_SECOND_IN_MS*time - TIME_HANDLE, lambda: frame_to_open.open())
	waiting_screen.after(ONE_SECOND_IN_MS*time, lambda : waiting_frame.destroy())


def leaderboard_read():
	''' :info: 	  A function used to read the leaderboard from the external leaderboard.txt file
		:inputs:  No Inputs in this function
		:outputs: Returns a list of all the saved game scores '''
	file = open('leaderboard.txt', 'r')
	send = file.readlines()
	file.close()
	return [[int(e[0])] + e[1:] for e in [score.split() for score in send]]


def settings_read(froms = 0, to = 9):
	''' :info: 	  A function used to read settings from the external settings.txt file
		:inputs:  It takes as inputs: "froms" being the index of the starting line in external settings.txt file, by default: 0 (first line), and "to" being the last line to consider from this file, by default 9 (last line)
		:outputs: Returns a dictionnary with setting_names as keys and setting_values as values '''
	dictionnary = {}
	file = open('settings.txt')
	send = file.readlines()
	file.close()
	for pair in send:
		if not pair == send[-1]: pair = pair[:-1] # if not the last pair
		index = pair.find(':')
		setting = pair[:index]
		value = pair[index+1:]
		dictionnary[setting] = value
	return dict(list(dictionnary.items())[froms:to])


def settings_write(setting_name, new_value):
	''' :info: 	  A function used to write settings to the external settings.txt file
		:inputs:  It takes as inputs: "setting_name" to edit, "new_value" to set
		:outputs: No returns from this function '''
	receive = settings_read()
	for setting in receive:
		if setting == setting_name:
			receive[setting] = new_value
			break
	receive = [list(item) for item in receive.items()]
	file = open('settings.txt', 'a')
	file.truncate(0)
	for line in receive:
		if not receive[-1] == line: file.write(":".join(line)+'\n')
		else: file.write(":".join(line))
	file.close()




