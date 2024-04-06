from ursina import *

class Particle(Entity):
    def __init__(self, lifespan=1, velocity=Vec2(0, 0), start_scale=.5, end_scale=1, scale_curve=curve.linear_boomerang, start_color=color.gold, end_color=color.hsv(0,0,.3), color_curve=curve.linear, **kwargs):
        if callable(velocity):
            velocity = velocity()
        self.velocity = velocity
        if callable(start_color):
            start_color = start_color()
        if callable(end_color):
            end_color = end_color()
        super().__init__(model="quad", texture="circle", scale=start_scale, color=start_color, unlit=True)
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
        self.look_at(-camera.world_position)


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
                self.particles.append(Particle(position=self.world_position, **self.particle_args))
        
    def pause(self):
        self.active = not self.active
    


if __name__ == "__main__":

    app = Ursina()
    from random import random, choice
    
    def velocity_setter():
        return Vec2(random()*.5-random()*.5, abs(random()-.1))
    def start_color_setter():
        return choice([color.rgb32(254, 222, 23), color.rgb32(255, 119, 0)])
    emiter = ParticleEmitter(velocity=velocity_setter, start_color=start_color_setter, y=.5)

    def input(key):
        if key == 'p':
            emiter.pause()

    EditorCamera()
    
    app.run()
