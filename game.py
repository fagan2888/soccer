import arcade, math, random, pymunk

screen_w, screen_h = 1000, 600

class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        #PHYSICS PYMUNK
        self.space = pymunk.Space()
        self.space.gravity = (0, -900)

        #Create the floor
        self.floor_height = 80
        floor = pymunk.Body(body_type = pymunk.Body.STATIC)
        shape = pymunk.Segment(floor, [0, self.floor_height], [screen_w, self.floor_height], 0)
        #maybe don't need friction?
        shape.friction = 10
        self.space.add(shape)



    def drop_ball(self):
        #not sure how this will work with pymunk
        self.ball = arcade.Sprite('images/soccer-ball.png', .1)
        self.ball.change_angle = .1
        # self.ball = pymunk.Body()

        pass

    def setup(self):
        #BALL
        self.drop_ball()
        #PLAYERS
        spawn_height = screen_h / 3
        self.player_list = arcade.SpriteList()
        #Player 1
        self.player1 = arcade.Sprite('kenney/PNG/Player/Poses/player_stand.png', 1.2)
        self.player1.center_x = screen_w * .25
        self.player1.center_y = spawn_height
        self.player1.textures = [arcade.load_texture('kenney/PNG/Player/Poses/player_stand.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Player/Poses/player_kick.png', 0, 0, 80, 110)]
        self.player1.update_animation = update_animation
        self.player_list.append(self.player1)
        #Player 2
        self.player2 = arcade.Sprite('kenney/PNG/Adventurer/Poses/adventurer_stand.png', 1.2)
        self.player2.center_x = screen_w * .40
        self.player2.center_y = spawn_height
        self.player2.textures = [arcade.load_texture('kenney/PNG/Adventurer/Poses/adventurer_stand.png', 0, 0, 80, 110), \
            arcade.load_texture('kenney/PNG/Adventurer/Poses/adventurer_kick.png', 0, 0, 80, 110)]
        self.player2.update_animation = update_animation
        self.player_list.append(self.player2)
        #Player 3
        self.player3 = arcade.Sprite('kenney/PNG/Female/Poses/female_stand_rev.png', 1.2)
        self.player3.center_x = screen_w * .60
        self.player3.center_y = spawn_height
        self.player3.textures = [arcade.load_texture('kenney/PNG/Female/Poses/female_stand_rev.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Female/Poses/female_kick_rev.png', 0, 0, 80, 110)]
        self.player3.update_animation = update_animation
        self.player_list.append(self.player3)
        #Player 4
        self.player4 = arcade.Sprite('kenney/PNG/Zombie/Poses/zombie_stand_rev.png', 1.2)
        self.player4.center_x = screen_w * .75
        self.player4.center_y = spawn_height
        self.player4.textures = [arcade.load_texture('kenney/PNG/Zombie/Poses/zombie_stand_rev.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Zombie/Poses/zombie_kick_rev.png', 0, 0, 80, 110)]
        self.player4.update_animation = update_animation
        self.player_list.append(self.player4)

    def on_draw(self):
        arcade.start_render()
        draw_sky()
        draw_grass()
        square_goal(20, 320)
        square_goal(screen_w - 160, 320)
        # self.ball.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            for player in self.player_list:
                if player.center_y == self.floor_height:
                    player.update_animation(player, 1)
                    #ADD PYMUNK THING TO MAKE THEM JUMP
                    # player.change_y = jump_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            for player in self.player_list:
                player.update_animation(player, 0)

    def update(self, delta_time):
        self.space.step(delta_time)
        #BALL STUFF
        # self.ball.update()
        # if self.ball.center_x > screen_w - 140 or self.ball.center_x < 140:
        #     #GOAL MECHANISM
        #     if self.ball.center_y < 300:
        #         #GOAL
        #         pass
        #     self.drop_ball()
        # if (self.ball.center_y > screen_h - 10 or self.ball.center_y < 40):
        #     self.ball.change_y = 0
        #     self.player_list.update()

        #PLAYER STUFF
        for player in self.player_list:
            if player.center_y >= 200:
                player.center_y = self.floor_height
            if player.center_y <= self.floor_height:
                player.center_y = self.floor_height
            if player.center_x >= screen_w - 200:
                player.center_x = screen_w-200
            if player.center_x <= 200:
                player.center_x = 200


#gravity and jump mechanism for players
#collision for ball
#kick mechanism for players

#BACKGROUND
grass_height = screen_h / 4

def draw_sky():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, screen_h, grass_height, arcade.color.CAPRI)

def draw_grass():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, grass_height, 0, arcade.color.FOREST_GREEN)

#SQUARE GOAL
def square_goal(top_left_x, top_left_y):
    #top part of goal
    arcade.draw_commands.draw_line(top_left_x, top_left_y, top_left_x + 140,
            top_left_y, arcade.color.BLUE_SAPPHIRE, 5)
    #back side of goal
    arcade.draw_commands.draw_line(top_left_x, top_left_y, top_left_x,
            top_left_y - 300, arcade.color.BLUE_SAPPHIRE, 5)
    #front side of goal
    arcade.draw_commands.draw_line(top_left_x + 140, top_left_y, top_left_x + 140,
            top_left_y - 300, arcade.color.BLUE_SAPPHIRE, 5)
    #bottom side of goal
    arcade.draw_commands.draw_line(top_left_x, top_left_y - 300, top_left_x + 140,
            top_left_y - 300, arcade.color.BLUE_SAPPHIRE, 5)
    for num in range(1, 140 // 20):
        arcade.draw_commands.draw_line(top_left_x + num * 20, top_left_y, top_left_x + num * 20,
                top_left_y - 300, arcade.color.WHITE, 2)
    for num in range(2, 300 // 20 + 1):
        arcade.draw_commands.draw_line(top_left_x, num * 20, top_left_x + 140,
                num * 20, arcade.color.WHITE, 2)

#UPDATE ANIMATION FOR PLAYERS
def update_animation(self, texture):
    self.set_texture(texture)

def main():
    game = MyGame(screen_w, screen_h)
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
