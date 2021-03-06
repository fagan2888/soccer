import arcade, math, random, pymunk

screen_w, screen_h = 1000, 600

#Physics
movement_speed = 5
jump_speed = 6
gravity = 1

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        #create sprite lists here and set to None
        self.player_list = None
        self.space = pymunk.Space()
        self.space.gravity = 0, -1000
        #set up player info
    def start_snowfall(self):
        self.snowflake_list = []
        for i in range(100):
            #create snowflake instance
            snowflake = Snowflake()

            #randomly position snowflake
            snowflake.x = random.randrange(screen_w)
            snowflake.y = random.randrange(screen_h + 200)

            #other variables for snowflake
            snowflake.size = random.randrange(4)
            snowflake.speed = random.randrange(20, 40)
            snowflake.angle = random.uniform(math.pi, math.pi * 2)

            #add snowflake to snowflake_list
            self.snowflake_list.append(snowflake)
    def drop_ball(self):
        self.ball = arcade.Sprite('images/soccer-ball.png', .1)
        self.ball.center_x = screen_w / 2
        self.ball.center_y = screen_h / 3
        direction = random.randint(0, 10)
        if direction // 5 > 0:
            self.ball.change_x = -3
        else:
            self.ball.change_x = 3
        self.ball.change_y = -10

    def setup(self):
        #set up game here
        self.drop_ball()
        self.ball_pymunk = pymunk.Body(3, 1666)
        self.space.add(self.ball_pymunk)
        #PLAYERS
        start_height = screen_h / 3
        #Player 1
        self.player_list = arcade.SpriteList()
        self.player1 = arcade.Sprite('kenney/PNG/Player/Poses/player_stand.png', 1.2)
        self.player1.center_x = screen_w / 4
        self.player1.center_y = start_height
        self.player1.textures = [arcade.load_texture('kenney/PNG/Player/Poses/player_stand.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Player/Poses/player_kick.png', 0, 0, 80, 110)]
        self.player1.update_animation = update_animation
        self.player_list.append(self.player1)
        #Player 2
        self.player2 = arcade.Sprite('kenney/PNG/Adventurer/Poses/adventurer_stand.png', 1.2)
        self.player2.center_x = screen_w / 4 + 100
        self.player2.center_y = start_height
        self.player2.textures = [arcade.load_texture('kenney/PNG/Adventurer/Poses/adventurer_stand.png', 0, 0, 80, 110), \
            arcade.load_texture('kenney/PNG/Adventurer/Poses/adventurer_kick.png', 0, 0, 80, 110)]
        self.player2.update_animation = update_animation
        self.player_list.append(self.player2)
        #Player 3
        self.player3 = arcade.Sprite('kenney/PNG/Female/Poses/female_stand_rev.png', 1.2)
        self.player3.center_x = 3 * screen_w / 4
        self.player3.center_y = start_height
        self.player3.textures = [arcade.load_texture('kenney/PNG/Female/Poses/female_stand_rev.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Female/Poses/female_kick_rev.png', 0, 0, 80, 110)]
        self.player3.update_animation = update_animation
        self.player_list.append(self.player3)
        #Player 4
        self.player4 = arcade.Sprite('kenney/PNG/Zombie/Poses/zombie_stand_rev.png', 1.2)
        self.player4.center_x = 3 * screen_w / 4 - 100
        self.player4.center_y = start_height
        self.player4.textures = [arcade.load_texture('kenney/PNG/Zombie/Poses/zombie_stand_rev.png', 0, 0, 80, 110), \
                arcade.load_texture('kenney/PNG/Zombie/Poses/zombie_kick_rev.png', 0, 0, 80, 110)]
        self.player4.update_animation = update_animation
        self.player_list.append(self.player4)

        self.physics_list = []
        for player in self.player_list:
            player.change_y = -10
            self.physics_list.append(arcade.PhysicsEnginePlatformer(player, self.player_list , gravity_constant = gravity))

    def on_draw(self):
        #render the screen
        arcade.start_render()
        #render should initiate before we start drawing - it will clear the
        #screen to background color and erase what was drawn
        draw_sky()
        draw_grass()
        square_goal(20, 320)
        square_goal(screen_w - 160, 320)
        #now call draw on all sprite lists
        self.ball.draw()
        for player in self.player_list:
            player.draw()
        for snowflake in self.snowflake_list:
            arcade.draw_circle_filled(snowflake.x, snowflake.y, snowflake.size,
                arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        #called whenever key is pressed
        if key == arcade.key.UP:
            for player in self.player_list:
                if player.center_y == 80:
                    player.update_animation(player,1)
                    player.change_y = jump_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            for player in self.player_list:
                player.update_animation(player,0)

    def update(self, delta_time):
        #game logic
        #animate snowflakes falling
        for snowflake in self.snowflake_list:
            snowflake.y -= snowflake.speed * delta_time

            #check if snowflake has fallen below screen
            if snowflake.y < 0:
                snowflake.reset_pos()
            #move side to side
            snowflake.x += snowflake.speed * math.cos(snowflake.angle) * delta_time
            snowflake.angle += delta_time
        self.ball.update()
        if self.ball.center_x > screen_w - 140 or self.ball.center_x < 140:
            #GOAL MECHANISM
            if self.ball.center_y < 300:
                #GOAL
                pass
            self.drop_ball()
        if (self.ball.center_y > screen_h - 10 or self.ball.center_y < 40):
            self.ball.change_y = 0
        # self.ball.change_x = 5
        for engine in self.physics_list:
            engine.update()
        self.player_list.update()
        for player in self.player_list:
            if player.center_y >= 200:
                player.center_y = 80
            if player.center_y <= 80:
                player.center_y = 80
            if player.center_x >= screen_w - 200:
                player.center_x = screen_w-200
            if player.center_x <= 200:
                player.center_x = 200
            # if len(arcade.check_for_collision_with_list(player, self.player_list))>0:
            #     player.change_x = 0

#Physics pymunk


#BACKGROUND
grass_height = screen_h / 4

def draw_sky():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, screen_h, grass_height, arcade.color.CAPRI)

def draw_grass():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, grass_height, 0, arcade.color.FOREST_GREEN)

#SNOW
class Snowflake:
    #each instance is a separate Snowflake
    def __init__(self):
        self.x = 0
        self.y = 0
    def reset_pos(self):
        #go to a random position
        self.x = random.randrange(screen_w)
        self.y = random.randrange(screen_h, screen_h + 100)

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
    game.start_snowfall()
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
