import arcade, math, random

screen_w, screen_h = 1000, 600

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        # arcade.set_background_color(arcade.color.AMAZON)

        #create sprite lists here and set to None
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

    def setup(self):
        #set up game here
        self.ball = arcade.Sprite('images/soccer-ball.png', .1)
        self.ball.center_x = screen_w / 2
        self.ball.center_y = screen_h / 3

    def on_draw(self):
        #render the screen
        arcade.start_render()
        #command should initiate before we start drawing - it will clear the
        #screen to background color and erase what was drawn
        draw_sky()
        draw_grass()
        draw_goal(150, 400, 20, 320)
        draw_goal(screen_w - 150, 400, screen_w - 20, 320)
        self.ball.draw()

        for snowflake in self.snowflake_list:
            arcade.draw_circle_filled(snowflake.x, snowflake.y, snowflake.size,
                arcade.color.WHITE)
        #now call draw on all sprite lists

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
        if (self.ball.center_y > screen_h - 10 or self.ball.center_y < 25 or
            self.ball.center_x > screen_w -10 or self.ball.center_x <5):
            pass
        else:
            self.ball.center_y -= 5
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

#GOAL
def draw_goal(front_high_x, front_high_y, back_high_x, back_high_y):
    #top part of goal
    arcade.draw_commands.draw_line(front_high_x, front_high_y, back_high_x, back_high_y,
            arcade.color.BLUE_SAPPHIRE, 5)
    #back side of goal
    arcade.draw_commands.draw_line(back_high_x, back_high_y, back_high_x, back_high_y - 300,
            arcade.color.BLUE_SAPPHIRE, 5)
    #front side of goal
    arcade.draw_commands.draw_line(front_high_x, front_high_y, front_high_x, back_high_y - 300,
            arcade.color.BLUE_SAPPHIRE, 5)
    #bottom of goal
    arcade.draw_commands. draw_line(front_high_x, back_high_y - 300, back_high_x, back_high_y - 300,
            arcade.color.BLUE_SAPPHIRE, 5)

def main():
    game = MyGame(screen_w, screen_h)
    game.setup()
    game.start_snowfall()
    arcade.run()

if __name__ == '__main__':
    main()
