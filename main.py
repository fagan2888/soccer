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
        pass

    def on_draw(self):
        #render the screen
        arcade.start_render()
        #command should initiate before we start drawing - it will clear the
        #screen to background color and erase what was drawn
        draw_sky()
        draw_grass()
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

grass_height = screen_h / 4

def draw_sky():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, screen_h, grass_height, arcade.color.CAPRI)

def draw_grass():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, grass_height, 0, arcade.color.FOREST_GREEN)

class Snowflake:
    #each instance is a separate Snowflake
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        #go to a random position
        self.x = random.randrange(screen_w)
        self.y = random.randrange(screen_h, screen_h + 100)


def main():
    game = MyGame(screen_w, screen_h)
    game.setup()
    game.start_snowfall()
    arcade.run()

if __name__ == '__main__':
    main()
