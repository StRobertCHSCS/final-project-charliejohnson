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
    arcade.draw_texture_rectangle(400,300,400,300,texture)
    texture1 = arcade.load_texture("images/start.png")
    arcade.draw_texture_rectangle(200,300,224,225,texture1)
    arcade.draw_text("AIRCRAFT BATTLE",300,450,arcade.color.WHITE,20)
def gameover():
    arcade.draw_text("Game Over", 300, 300, arcade.color.WHITE, 40)

if current_state == INSTRUCTIONS_PAGE_0:
    start_page()
elif current_state == GAME_OVER:
    gameover()

def main():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing with Functions")
    arcade.set_background_color(arcade.color.DARK_BLUE)
    arcade.start_render()




    # Finish and run
    arcade.finish_render()
    arcade.run()


# Call the main function to get the program started.
main()

