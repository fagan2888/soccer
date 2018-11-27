import arcade, math, random, pymunk

from constants import *


class PhysicsSprite(arcade.Sprite):
    def __init__(self,
                 filename,
                 center_x=0,
                 center_y=0,
                 scale=1,
                 mass=default_mass,
                 moment=None,
                 friction=default_friction,
                 body_type=pymunk.Body.DYNAMIC):

        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)

        width = self.texture.width * scale
        height = self.texture.height * scale

        if moment is None:
            moment = pymunk.moment_for_box(mass, (width, height))

        self.body = pymunk.Body(mass, moment, body_type=body_type)
        self.body.position = pymunk.Vec2d(center_x, center_y)

        #need to change this to a polygon for 
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.friction = friction

def resync_physics_sprites(sprite_list):
    """ Move sprites to where physics objects are """
    for sprite in sprite_list:
        sprite.center_x = sprite.shape.body.position.x
        sprite.center_y = sprite.shape.body.position.y
        sprite.angle = math.degrees(sprite.shape.body.angle)
