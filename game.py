import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from math import *

k=100
k_position = 0.01*k
k_velocity = 0
k_angle_penalty = 0
k_velocity_penalty = 0
k_theta = k
k_omega = 0


class Vehicle:
    def __init__(self, x, y, scaling=1, angle_0=0.0, length_0=4, max_steering_0=30, max_acceleration_0=5.0, k_steering_0=30, brake_deceleration_0=10, free_deceleration_0=2, max_velocity_0=20):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle_0
        self.length = length_0
        self.max_acceleration = max_acceleration_0
        self.max_steering = max_steering_0
        self.max_velocity = max_velocity_0/scaling
        self.brake_deceleration = brake_deceleration_0
        self.free_deceleration = free_deceleration_0
        self.k_steering = k_steering_0
        self.scaling = scaling

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        # User input
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += (1/self.scaling) * dt
        elif pressed[pygame.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= (1/self.scaling) * dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        #steering
        if pressed[pygame.K_RIGHT]:
            self.steering -= self.k_steering * dt
        elif pressed[pygame.K_LEFT]:
            self.steering += self.k_steering * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        #velocity update
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))


        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
    
    def draw(self, car_image, ppu, game):
        rotated_car = pygame.transform.rotate(car_image, self.angle)
        rect = rotated_car.get_rect()
        game.screen.blit(rotated_car, self.position * ppu - (rect.width / 2, rect.height / 2))
        return


class Drone:
    def __init__(self, x, y, scaling=1, angle_0=0, length_0=4, max_steering_0=30, max_acceleration_0=5.0, k_steering_0=30,
                 brake_deceleration_0=10, free_deceleration_0=2, max_velocity_0=20, min_velocity_0=0,
                 target_position_0=Vector2(0,0)):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle_0
        self.length = length_0
        self.max_acceleration = max_acceleration_0
        self.max_steering = max_steering_0
        self.max_velocity = max_velocity_0/scaling
        self.min_velocity = min_velocity_0/scaling
        self.brake_deceleration = brake_deceleration_0
        self.free_deceleration = free_deceleration_0
        self.k_steering = k_steering_0
        try:
            self.previous_theta = acos(Vector2.dot(target_position_0, Vector2(1.0, 0.0))/Vector2.magnitude(target_position_0)) - self.angle
        except:
            self.previous_theta = 0
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt, target_position, target_velocity):
        #deltas
        del_position = Vector2.magnitude(target_position - self.position)
        del_velocity = Vector2.magnitude(target_velocity - self.velocity)

        u = Vector2.normalize(target_position - self.position)
        u_x = Vector2(1.0, 0.0).rotate(self.angle)
        u_y = Vector2(0.0, 1.0).rotate(self.angle)
        cross_product = Vector2.cross(u, u_x)
        #theta = asin(cross_product)

        #theta = atan2(u.x*u_x.y - u_x.x*u.y, u.x*u.y - u_x.x*u_x.y)
        x = Vector2.dot(u, u_x)
        y = Vector2.dot(u, u_y)
        theta = atan(y/x)
        
        theta = Vector2.angle_to(u, u_x)
        print(theta)

        

        #theta = atan(radians(target_position.y/target_position.x))
        
        #print(target_position.y, target_position.x)
        del_theta = (theta - self.previous_theta)

        self.previous_theta = theta

        #Gaz pedal controller
        self.acceleration = k_position*del_position + k_velocity*del_velocity - k_angle_penalty*sin(radians(self.angle))**2
        self.acceleration = 0
        #steering controller
        self.steering = k_theta*theta + k_omega*del_theta - k_velocity_penalty*Vector2.magnitude(self.velocity)/self.max_velocity
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        #velocity update
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(self.min_velocity, min(self.velocity.x, self.max_velocity))


        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
    
    def draw(self, drone_image, ppu, game):
        rotated_drone = pygame.transform.rotate(drone_image, self.angle)
        rect = rotated_drone.get_rect()
        game.screen.blit(rotated_drone, self.position * ppu - (rect.width / 2, rect.height / 2))
        return


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Drone pursuit")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        car_image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(car_image_path)
        taille = car_image.get_size()
        scaling = 10
        taille = [taille[0]/scaling, taille[1]/scaling]
        car_image = pygame.transform.scale(car_image, taille)
        car = Vehicle(x=2, y=0, scaling=scaling)
        drone = Drone(x=10, y=10, scaling=scaling)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Logic
            car.update(dt)

            drone.update(dt, target_position=car.position, target_velocity=car.velocity)
            
            # Drawing
            self.screen.fill((0, 0, 0))
            car.draw(car_image, ppu, self)
            drone.draw(car_image, ppu, self)
            
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
