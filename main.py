import arcade

screen_w, screen_h = 1000, 600

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        # arcade.set_background_color(arcade.color.AMAZON)

        #create sprite lists here and set to None
    def setup(self):
        #set up game here
        pass
    def on_draw(self):
        #render the screen
        #command should initiate before we start drawing - it will clear the
        #screen to background color and erase what was drawn
        arcade.start_render()
        draw_sky()
        draw_grass()
        #now call draw on all sprite lists
    def update(self, delta_time):
        #game logic
        pass

def draw_sky():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, screen_h, (3*screen_h)/4, arcade.color.CAPRI)

def draw_grass():
    arcade.draw_lrtb_rectangle_filled(0, screen_w, (3*screen_h)/4, 0, arcade.color.FOREST_GREEN)

def main():
    game = MyGame(screen_w, screen_h)
    game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
