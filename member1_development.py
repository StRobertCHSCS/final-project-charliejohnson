import arcade
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Python Arcade Game: StormPlane"
BULLET_SPEED = 2
Score = 0

INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

explode = 0
explode_x = 0
explode_y = 0
fps = 0
boss_create_fps = 0

position_y_1 = 600
position_y_2 = 0

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

class Enemy(arcade.Sprite):
    # pass attribute to enemy
    def __init__(self, image, scale, ehp, score, speed, boss):
        """
        Initialize an enemy with information passed in.

        :param image: enemy image
        :param scale: enemy scale
        :param ehp: enemy hit points
        :param score: kill enemy score
        :param speed: enemy speed
        :param boss: enemy type, True when he is boss
        """
        arcade.Sprite.__init__(self, image, scale)
        self.ehp = ehp
        self.score = score
        self.speed = speed
        self.boss = boss
        self.left_boss = True

    # self armo damage, hhp
    def hitted(self, hhp):
        """
        Enemy hit by self bullet. Return boss kill information and killed coordinates.

        :param hhp: self bullet damage to the enemy
        :return: Tuple, represents boss killed(1), otherwise(0); killed xy coordinates in order.
        """
        global Score
        self.ehp = max(0, self.ehp - hhp)
        if self.ehp == 0:
            self.kill()
            Score += self.score
            if self.boss:

                return (1, self.center_x, self.center_y)
        return (0, 0, 0)

    def drop(self):
        """
        Update enemy location
        :return: None
        """
        if self.boss and self.center_y <= 450:

            if self.center_x <= 100:
                self.left_boss = False

            if self.center_x >= 700:
                self.left_boss = True

            if self.left_boss:
                self.center_x -= 2
            else:
                self.center_x += 2

            if self.center_x == 100:
                self.left_boss = False
            if self.center_x == 700:
                self.left_boss = True

        else:
            self.center_y -= self.speed

        if self.center_y < 0:
            self.kill()


class MyGame(arcade.Window):
    """ Main application class """

    def __init__(self, width, height, title):
        """
        Initialize the game window
        :param width: window width
        :param height: window height
        :param title: window title
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.

        self.frame_count = 0
        self.hp = 100
        self.boss = False
        self.laser_player = 0

        self.enemy_list = None
        self.bullet_list = None
        self.bullet_self_list = None
        self.player_list = None
        self.player = None
        self.assist = None
        self.bonus = None

        # self.current_state = INSTRUCTIONS_PAGE_0
        #
        # self.instructions = []
        # texture = arcade.load_texture("images/name.png")
        # self.instructions.append(texture)
        #
        # texture = arcade.load_texture("images/start.png")
        # self.instructions.append(texture)

    def on_draw(self):
        """Render the screen.
        :return: None
        """
        global Score, position_y_1, position_y_2, level, prompt, boss_hp, boss_hp_current, laser_effect, INSTRUCTIONS_PAGE_0, INSTRUCTIONS_PAGE_1
        global GAME_RUNNING, GAME_OVER
        arcade.start_render()
        texture_0 = arcade.load_texture("images/bigairplane3.png")

        # if self.current_state == INSTRUCTIONS_PAGE_0:
        #     self.draw_instructions_page(0)
        #
        # elif self.current_state == INSTRUCTIONS_PAGE_1:
        #     self.draw_instructions_page(1)
        #
        # elif self.current_state == GAME_RUNNING:
        #     self.draw_game()
        #
        # else:
        #     self.draw_game()
        #     self.draw_game_over()

        # Draw background and boss for each level
        if level == 0:
            texture_1 = arcade.load_texture("images/bg_0.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_0.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_2.png")

        if level == 1:
            texture_1 = arcade.load_texture("images/bg_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_4.png")

        if level == 2:
            texture_1 = arcade.load_texture("images/bg6.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg6.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_1.png")

        if level == 3:
            texture_1 = arcade.load_texture("images/bg4.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg4.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_5.png")

        # draw images
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.bullet_self_list.draw()
        self.assist.draw()
        self.bonus.draw()

        # boss killed explode animation
        if explode == 1:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane3.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 2:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane4.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 3:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane5.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 4:
            texture_0 = arcade.load_texture("images/bg_road.png")
            arcade.draw_texture_rectangle(400, 300, 450, 430, texture_0)




        # Draw different boss lasers
        for b in self.enemy_list:
            if level == 0:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser11.png"))

            if level == 1:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser11.png"))

            if level == 2:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x - 40 , b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y-300, 30, 600, arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))

            if level == 3:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))



        if prompt:
            arcade.draw_texture_rectangle(400, 350, 300, 200, arcade.load_texture("images/boss_prompt.png"))


        if self.boss:
            arcade.draw_lrtb_rectangle_outline(300, 500, 580, 560, arcade.color.BLACK, 2)
            arcade.draw_lrtb_rectangle_filled(302, 302 + (198 * boss_hp_current) // boss_hp, 578, 562, arcade.color.RADICAL_RED)

        arcade.draw_text("Score: {0:10.2f}".format(Score), 610, 560, arcade.color.WHITE, 12)
        arcade.draw_lrtb_rectangle_outline(60, 170, 580, 560, arcade.color.WHITE, 2)
        arcade.draw_lrtb_rectangle_filled(62, 62 + (106*self.hp)//100, 578, 562, arcade.color.WHITE)
        arcade.draw_text("HP: {0:10.2f}%".format(self.hp), 180, 562, arcade.color.WHITE, 12)
        if self.laser_player >= 1:
            for i in range(self.laser_player):
                arcade.draw_texture_rectangle(760 - i * 50, 520, 50, 40, arcade.load_texture("images/missile_icon.png"))



    def setup(self):
        """
        Initialize game interface. Default schedule is 60 fps.
        :return: None
        """
        arcade.schedule(self.on_update, 1/60)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()
        self.assist = arcade.SpriteList()
        self.bonus = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("images/SeHero.png", 0.6)

        self.player_list.append(self.player)

    #     self.set_mouse_visible(False)
    #
    # def draw_instructions_page(self, page_number):
    #
    #     page_texture = self.instructions[page_number]
    #     arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, page_texture.width, page_texture.height, page_texture, 0)
    #
    # def draw_game_over(self):
    #
    #     output = "Game Over"
    #     arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)
    #
    #     output = "Click to restart"
    #     arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

        # 掉道具
        # for _ in range(2):
        #     # generate random x and y values
        #     enemy = arcade.Sprite("images/plane.png", 0.5)
        #     enemy.center_x = random.randrange(0, SCREEN_WIDTH)
        #     enemy.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
        #     enemy.angle = 180
        #     self.enemy_list.append(enemy)


        # 子弹与飞机
        # 吃道具


    def dead(self):
        """
        Clear the screen when dead
        :return: None
        """
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()



    def update(self, delta_time):
        """All the logic to move, and the game logic goes here. """
        global explode, explode_x, explode_y, fps, position_y_1, position_y_2, level, prompt, prompt_time, boss_hp, boss_hp_current
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb, laser_effect, laser_fps, laser_counter, laser_counter_update
        global boss_create_fps

        if True:
            laser_counter = Score // 1000 + 1
            if laser_counter + laser_counter_update == 1:
                self.laser_player += 1
                laser_counter_update -= 1

            if self.hp <= 0:
                self.dead()
            else:
                # drop hp bonus every 60s
                if self.frame_count % 3600 == 3599:
                    bonus_hp = arcade.Sprite("images/hp_bonus.png", 0.6)
                    bonus_hp.center_x = random.randrange(0, SCREEN_WIDTH)
                    bonus_hp.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                    self.bonus.append(bonus_hp)


                if self.frame_count % 180 == 0 and not self.boss and not 1 <= explode <= 4:
                    for _ in range(2):
                    # generate random enemy planes
                        ranNum = random.randint(0, 1000)
                        if ranNum < 500:
                            enemy = Enemy("images/plane_small.png", 0.8, 2, 10, 4, False)
                        elif ranNum < 850:
                            enemy = Enemy("images/bigplane0.png", 0.7, 3, 50, 3, False)
                        else:
                            enemy = Enemy("images/boss0.png", 0.35, 5, 100, 2, False)


                        enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                        enemy.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                        enemy.angle = 180
                        self.enemy_list.append(enemy)

                # create a boss and ensure no small enemies appear during the boss battle
                elif self.frame_count - fps == (1799*(level+1)) and not self.boss and not 1 <= explode <= 4:
                    # 提示
                    boss_create_fps = self.frame_count
                    prompt = True
                    prompt_time = self.frame_count

                    # update boss based on game level
                    if level == 0:
                        enemy = Enemy("images/boss_2.png", 0.8, 20, 500, 2, True)
                    elif level == 1:
                        enemy = Enemy("images/boss_4.png", 0.8, 30, 1000, 3, True)
                    elif level == 2:
                        enemy = Enemy("images/boss_1.png", 0.8, 40, 2000, 3, True)
                    elif level == 3:
                        enemy = Enemy("images/boss_5.png", 0.8, 50, 4000, 3, True)


                    enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                    enemy.center_y = SCREEN_HEIGHT * 2
                    enemy.angle = 180
                    self.enemy_list.append(enemy)
                    self.boss = True
                    boss_hp = enemy.ehp

                # set time for boss prompt to be 3s
                if self.frame_count - prompt_time == 180 and prompt:
                    prompt = False

                for boss in self.enemy_list:
                    if 1 <= laser_effect <= 6:
                        for e in self.bullet_self_list:
                            # kill self bullet
                            if boss.center_x - 20 <= e.center_x <= boss.center_x + 20:
                                e.kill()
                        # hit by laser --- lose hp
                        if level == 0:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 0.8)
                        if level == 1:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 0.9)
                        if level == 2:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1)
                        if level == 3:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1.1)

                    # for e in self.enemy_list:
                    #     if self.player.center_x - 40 <= e.center_x <= self.player.center_x + 40:
                    #         boss_hit = e.hitted(20)
                    #         if boss_hit[0] == 1:
                    #             self.boss = False
                    #
                    #             lvl_clear = True
                    #
                    #             explode = 1
                    #             explode_x = boss_hit[1]
                    #             explode_y = boss_hit[2]
                    #             fps = self.frame_count

                # update the frame_count
                self.frame_count += 1

                # update the background position
                position_y_1 -= 1
                position_y_2 -= 1

                if position_y_1 == -300:
                    position_y_1 = 900
                if position_y_2 == -300:
                    position_y_2 = 900


                # collision with bullet
                bullet_collide_list = arcade.check_for_collision_with_list(self.player, self.bullet_list)
                for collide_bullet in bullet_collide_list:
                    collide_bullet.kill()
                    self.hp = max(0, self.hp - 5)

                # collision with enemy
                enemy_collide_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
                for collide_enemy in enemy_collide_list:
                    collide_enemy.kill()
                    if self.boss:
                        self.boss = False
                    self.hp = max(0, self.hp - 30)


                # hit enemy
                for e in self.enemy_list:
                    if e.boss:
                        boss_hp_current = e.ehp
                    bullet_hit_list = arcade.check_for_collision_with_list(e, self.bullet_self_list)
                    for bullet_hit in bullet_hit_list:
                        bullet_hit.kill()

                        boss_hit = e.hitted(1)
                        if boss_hit[0] == 1:
                            self.boss = False

                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                for bomb in self.assist:
                    bullet_hit_list = arcade.check_for_collision_with_list(bomb, self.bullet_list)

                    for b in bullet_hit_list:
                        b.kill()

                # collision with boss (missile)
                for e in self.enemy_list:
                    if e.boss:
                        boss_hp_current = e.ehp
                    bullet_hit_list = arcade.check_for_collision_with_list(e, self.assist)
                    for bullet_hit in bullet_hit_list:

                        boss_hit = e.hitted(0.3)
                        if boss_hit[0] == 1:
                            self.boss = False

                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                # boss explode animation
                if explode == 1 and self.frame_count - fps == 20:
                    explode += 1
                elif explode == 2 and self.frame_count - fps == 40:
                    explode += 1
                elif explode == 3 and self.frame_count - fps == 60:
                    explode += 1
                elif explode == 4 and self.frame_count - fps == 180:
                    explode += 1
                    level += 1

                # Loop through each enemy that we have
                for enemy in self.enemy_list:

                    # First, calculate the angle to the player. We could do this
                    # only when the bullet fires, but in this case we will rotate
                    # the enemy to face the player each frame, so we'll do this
                    # each frame.

                    # Position the start at the enemy's current location
                    start_x = enemy.center_x
                    start_y = enemy.center_y

                    # list_1[i][2]Get the destination location for the bullet
                    dest_x = self.player.center_x
                    dest_y = self.player.center_y

                    # Do math to calculate how to get the bullet to the destination.
                    # Calculation the angle in radians between the start points
                    # and end points. This is the angle the bullet will travel.
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)

                    # Set the enemy to face the player.
                    if self.boss:
                        enemy.angle = 0
                    else:
                        enemy.angle = math.degrees(angle)-90

                    # Shoot every 60 frames change of shooting each frame
                    # if self.frame_count % (120 - 20*level) == 0:
                    #     if self.boss:
                    #         bullet = arcade.Sprite("images/enemy_bullet.png", 0.5)
                    #     else:
                    #         bullet = arcade.Sprite("images/Bomb1.png", 0.5)
                    #     bullet.center_x = start_x
                    #     bullet.center_y = start_y
                    #
                    #     # Angle the bullet sprite
                    #     # Taking into account the angle, calculate our change_x
                    #     # and change_y. Velocity is how fast the bullet travels.
                    #     if self.boss:
                    #         bullet.angle = 0
                    #         bullet.change_x = 0
                    #         bullet.change_y = - BULLET_SPEED
                    #
                    #     else:
                    #         bullet.angle = math.degrees(angle)
                    #         bullet.change_x = math.cos(angle) * BULLET_SPEED
                    #         bullet.change_y = math.sin(angle) * BULLET_SPEED
                    #
                    #     self.bullet_list.append(bullet)

                    if self.boss and self.frame_count % ((120 - 20 * level) // 2) == 0:
                        bullet = arcade.Sprite("images/boss_bullet.png", 0.5)
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = 0
                        bullet.change_x = 0
                        bullet.change_y = - BULLET_SPEED * (level//3 + 1)
                        self.bullet_list.append(bullet)
                    elif self.frame_count % (120 - 20*level) == 0:
                        bullet = arcade.Sprite("images/enemy_bullet.png", 0.5)
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = math.degrees(angle)
                        bullet.change_x = math.cos(angle) * BULLET_SPEED * (level//3 + 1)
                        bullet.change_y = math.sin(angle) * BULLET_SPEED * (level//3 + 1)
                        self.bullet_list.append(bullet)

                # determine the shooting frequency
                if self.frame_count % 15 == 0:
                    bullet = arcade.Sprite("images/Bomb2.png", 0.7)
                    bullet.center_x = self.player.center_x
                    bullet.center_y = self.player.center_y

                    # Angle the bullet sprite
                    bullet.angle = 0

                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    bullet.change_x = 0
                    bullet.change_y = BULLET_SPEED * 3

                    self.bullet_self_list.append(bullet)

                # Get rid of the bullet when it flies off-screen
                for bullet in self.bullet_self_list:
                    if bullet.bottom > 600:
                        bullet.kill()

                for bullet in self.assist:
                    if bullet.bottom > 600:
                        bullet.kill()

                for bullet in self.bullet_list:
                    if bullet.top < 0:
                        bullet.kill()

                # hp_bonus
                for hp_bonus in self.bonus:
                    hp_bonus.center_y -= 5
                    if arcade.check_for_collision(self.player, hp_bonus):
                        self.hp = min(100, self.hp + 30)
                        hp_bonus.kill()
                    if hp_bonus.top < 0:
                        hp_bonus.kill()

                # keyboard control
                if up_pressed:
                    self.player.center_y = min(552, self.player.center_y + 5)
                if down_pressed:
                    self.player.center_y = max(48, self.player.center_y - 5)
                if left_pressed:
                    self.player.center_x = max(36, self.player.center_x - 5)
                if right_pressed:
                    self.player.center_x = min(764, self.player.center_x + 5)

                # trigger the missile
                if laser_bomb and self.laser_player > 0 and len(self.assist) <= 1:


                    assist_bomb = arcade.Sprite("images/assisent1_1.png", 1)
                    assist_bomb.center_x = self.player.center_x - 25
                    assist_bomb.center_y = self.player.center_y
                    assist_bomb.angle = 0
                    assist_bomb.change_x = 0
                    assist_bomb.change_y = 10
                    self.assist.append(assist_bomb)

                    assist_bomb = arcade.Sprite("images/assisent1_1.png", 1)
                    assist_bomb.center_x = self.player.center_x + 25
                    assist_bomb.center_y = self.player.center_y
                    assist_bomb.angle = 0
                    assist_bomb.change_x = 0
                    assist_bomb.change_y = 10
                    self.assist.append(assist_bomb)
                    self.laser_player -= 1

                if self.boss and (self.frame_count - boss_create_fps) % 480 == 0 and (self.frame_count - boss_create_fps) != 0:
                    laser_effect = 1
                    laser_fps = self.frame_count

                if self.frame_count % 60 == 0:
                    print(self.frame_count, boss_create_fps, laser_effect)


                if laser_effect == 1 and self.frame_count - laser_fps == 20:
                    laser_effect += 1
                elif laser_effect == 2 and self.frame_count - laser_fps == 40:
                    laser_effect += 1
                elif laser_effect == 3 and self.frame_count - laser_fps == 60:
                    laser_effect += 1
                elif laser_effect == 4 and self.frame_count - laser_fps == 80:
                    laser_effect += 1
                elif laser_effect == 5 and self.frame_count - laser_fps == 100:
                    laser_effect += 1
                elif laser_effect == 6 and self.frame_count - laser_fps == 120:
                    laser_effect += 1

                for e in self.enemy_list:
                    e.drop()

                # if level == 4:
                #     self.current_state = GAME_OVER
                #     self.set_mouse_visible(True)

                self.bullet_list.update()
                self.bullet_self_list.update()
                self.assist.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        :param x: player x-location
        :param y: player y-location
        :param delta_x: player delta x
        :param delta_y: player delta y
        :return: None
        """
        self.player.center_x = x
        self.player.center_y = y

    # def on_mouse_press(self, x, y, button, modifiers):
    #     """
    #     Called when the user presses a mouse button.
    #     """
    #
    #     # Change states as needed.
    #     if self.current_state == INSTRUCTIONS_PAGE_0:
    #         # Next page of instructions.
    #         self.current_state = INSTRUCTIONS_PAGE_1
    #     elif self.current_state == INSTRUCTIONS_PAGE_1:
    #         # Start the game
    #         self.setup()
    #         self.current_state = GAME_RUNNING
    #     elif self.current_state == GAME_OVER:
    #         # Restart the game.
    #         self.setup()
    #         self.current_state = GAME_RUNNING





    def on_key_press(self, key, modifier):
        """
        Detect user key input when a key is pressed

        :param key: the particular key user pressed
        :param modifier: default modifier
        :return: None
        """
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb
        if key == arcade.key.W:
            up_pressed = True
        if key == arcade.key.S:
            down_pressed = True
        if key == arcade.key.A:
            left_pressed = True
        if key == arcade.key.D:
            right_pressed = True
        if key == arcade.key.Z:
            laser_bomb = True


    def on_key_release(self, key, modifier):
        """
        Detect user key input when a key is released

        :param key: the particular key user released
        :param modifier: default modifier
        :return: None
        """
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb
        if key == arcade.key.W:
            up_pressed = False
        if key == arcade.key.S:
            down_pressed = False
        if key == arcade.key.A:
            left_pressed = False
        if key == arcade.key.D:
            right_pressed = False
        if key == arcade.key.Z:
            laser_bomb = False

# Variables to record if certain keys are being pressed.
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
