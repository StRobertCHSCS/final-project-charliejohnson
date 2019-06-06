import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Python Arcade Game: StormPlane"
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

current_state = INSTRUCTIONS_PAGE_0
def start_page():
    texture = arcade.load_texture("images/fm.png")
    arcade.draw_texture_rectangle(400,300,800,600,texture)
    texture1 = arcade.load_texture("images/start1.png")
    arcade.draw_texture_rectangle(400,200,224,225,texture1)
    arcade.draw_text("AIRCRAFT BATTLE",300,450,arcade.color.WHITE,20)
def gameover():
    arcade.draw_text("Game Over", 300, 300, arcade.color.WHITE, 40)

def main():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing with Functions")
    arcade.set_background_color(arcade.color.DARK_BLUE)
    arcade.start_render()

    if current_state == INSTRUCTIONS_PAGE_0:
        start_page()
    elif current_state == GAME_OVER:
        gameover()

    # Finish and run
    arcade.finish_render()
    arcade.run()


# Call the main function to get the program started.
main()

import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Python Arcade Game: StormPlane"
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3



def setup():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT,INSTRUCTIONS_PAGE_0,INSTRUCTIONS_PAGE_1,GAME_OVER,GAME_RUNNING, "My Arcade Game")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press

    arcade.run()


def update(delta_time):
    pass


def on_draw():
    arcade.start_render()
    # Draw in h


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()