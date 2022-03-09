''' This file contains the main game instructions of our game '''
#               Default Resolution : 1920 x 1080                #
# ------------------------------------------------------------- #


# --- Module imports ---
from tkinter import *
from myGame import Game_menu
from myAdds import settings_read
import myMenus as Menu


# --- Window initialising ---

# Ẁindow creation:
root = Tk()
root.title("COMP16321 Coursework - Flow")
# Menu Bar and Window Favicons:
root.call('wm', 'iconphoto', root._w, PhotoImage(file='Sprites/Icon/logo.png'))

# Window settings:
WINDOW_SIZE = (1920, 1080, 0, 0) # width, height, x_position, y_position (DO NOT change)

# - Window geometry -
is_fullscreen = eval(settings_read()['fullscreen'])
root.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
root.resizable(False, False) # Prevent user from resizing the window
root.attributes('-fullscreen', is_fullscreen)

# - Screen settings -
root.config(cursor = "plus", background="#ff8989") # Change cursor and background color



# --- Main Program ---

# Create all frames
game_frame = Frame(root, width = 1920, height = 1080, background="#ff8989")
game_frame.grid(row=0, column=0)
main_frame = Frame(root, width = 1920, height = 1080, background="#ff8989")
main_frame.grid(row=0, column=0)
opening_frame = Frame(root, width = 1920, height = 1080, background="#ff8989")
opening_frame.grid(row=0, column=0)

# Create all canvas (menus)
game_menu = Game_menu(game_frame)
play_menu = Menu.Play_menu(main_frame, game_menu)
video_menu = Menu.Video_menu(main_frame)
sound_menu = Menu.Sound_menu(main_frame)
controls_menu = Menu.Controls_menu(main_frame)
settings_menu = Menu.Settings_menu(main_frame, {'video': video_menu, 'sound': sound_menu, 'controls': controls_menu})
extras_menu = Menu.Extras_menu(main_frame)
start_menu = Menu.Start_menu(root, main_frame, {'play': play_menu, 'settings': settings_menu, 'extras': extras_menu})
opening_menu = Menu.Opening_menu(root, opening_frame, start_menu)



# --- Runtime ---

# Run de first menu of the game
opening_menu.open()

# mainloop call
root.mainloop()



