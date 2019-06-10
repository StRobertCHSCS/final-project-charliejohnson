import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Python Arcade Game: StormPlane"
BULLET_SPEED = 2
Score = 0

INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3
WIN = 4

position_y_1 = 600
position_y_2 = 0

explode = 0
explode_x = 0
explode_y = 0
fps = 0
boss_create_fps = 0

level = 0
# boss level prompt
prompt = False
prompt_time = 0

boss_hp = 0
boss_hp_current = 0

laser_bomb = False
laser_effect = 0
laser_fps = 0

# Calculate the remaining missile
laser_counter = 0
laser_counter_update = 0

background_sound = arcade.load_sound("music/supply.wav")
