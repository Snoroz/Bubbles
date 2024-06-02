from ursina import *

class Particle(Entity):
    def __init__(self, lifespan=1, velocity=Vec2(0, 0), start_scale=.5, end_scale=1, scale_curve=curve.linear_boomerang, start_color=color.white, end_color=color.white, color_curve=curve.linear, **kwargs):
        if callable(velocity):
            velocity = velocity()
        self.velocity = velocity
        if callable(start_color):
            start_color = start_color()
        if callable(end_color):
            end_color = end_color()
        super().__init__(model='quad.ursinamesh', scale=start_scale, color=start_color, unlit=True)
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except:
                print(key, value)

        self.animate_scale(value=end_scale, duration=lifespan, curve=scale_curve)
        self.animate_color(value=end_color, duration=lifespan, curve=color_curve)
        destroy(self, delay=lifespan)
        del self

    def update(self):
        self.position += self.velocity * time.dt


class ParticleEmitter(Entity):
    def __init__(self, frequency=.1, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities)
        self.active = True
        self.frequency = frequency
        self.particle_args = kwargs
        self.timer = 0
        self.particles = []
        
    def update(self):
        if self.active:
            self.timer += time.dt
            if self.timer >= self.frequency:
                self.timer = 0
                self.particles.append(Particle(parent=self, **self.particle_args))
        
    def pause(self):
        self.active = not self.active
    


if __name__ == "__main__":

    app = Ursina()
    from random import random, choice
    
    def start_color_setter():
        return choice([color.rgb32(254, 222, 23), color.rgb32(255, 119, 0)])
    def velocity_setter():
        return Vec2(.5*(random()-random()), abs(random()-.1))
    emitter = ParticleEmitter(texture='radial_gradient.png', start_color=start_color_setter, end_color=Vec4(color.dark_gray[0], color.dark_gray[1], color.dark_gray[2], 0), y=.5, velocity=velocity_setter)

    def input(key):
        if key == 'p':
            emitter.pause()

    EditorCamera()
    
    app.run()
