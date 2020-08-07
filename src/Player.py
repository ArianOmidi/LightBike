import pygame
from Trail import *
from LightBike import *


class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_pos, velocity):
        # Call parent class constructor
        super().__init__()

        self.color = color
        self.size = playerWidth
        self.lives = PLAYERLIVES

        self.powerup_active = False
        self.invulnerable = False
        self.color_change_time = 0

        self.init_velocity = velocity
        self.init_pos = start_pos

        self.image = getImages(self.color)[2 - sign(velocity)]

        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        self.velocity = (velocity, 0)
        self.activeTrail = None

        self.newTrail()

    # --- Abstract Classes --- #

    # def powerup(self):

    # def check_powerup(self):

    # --- Setters --- #

    def setImage(self, new_vel, color):
        change_x = change_y = 0
        old_pos = (self.rect.x, self.rect.y)

        if (new_vel[0] != 0):
            if (new_vel[0] < 0):
                self.image = getImages(color)[3]
                change_x = -playerWidth
            else:
                self.image = getImages(color)[1]

            if (self.velocity[1] > 0):
                change_y = playerWidth
        else:
            if (new_vel[1] < 0):
                self.image = getImages(color)[0]
                change_y = -playerWidth
            else:
                self.image = getImages(color)[2]

            if (self.velocity[0] > 0):
                change_x = playerWidth

        self.rect = self.image.get_rect()
        self.rect.x = old_pos[0] + change_x
        self.rect.y = old_pos[1] + change_y


    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity, self.cur_design)
        self.velocity = velocity
        self.newTrail()

    def setDesign(self, vel, color):
        self.cur_design = color

        if (vel[0] != 0):
            if (vel[0] < 0):
                self.image = getImages(color)[3]
            else:
                self.image = getImages(color)[1]
        else:
            if (vel[1] < 0):
                self.image = getImages(color)[0]
            else:
                self.image = getImages(color)[2]

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)

    # --- Death Classes --- #
    def death(self):
        self.lives -= 1

        self.image = EXPLOSION
        self.rect.x -= 6
        self.rect.y -= 6

        if (self.lives == 0):
            return True

        return False

    def reset(self):
        self.powerup_active = False

        self.image = getImages(self.color)[2 - sign(self.init_velocity)]


        self.velocity = (self.init_velocity, 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]

        self.newTrail()
        self.lastActiveTrail = None



    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (self.activeTrail is not None):
            self.activeTrail.update()

        if self.powerup_active:
            self.check_powerup()

    def powerup_time_warning(self):
        # Change Bike color to inform player that the powerup is running out
        # Color changes faster when there is less time
        if (self.powerup_time < POWERUPTIME * FPS / 1.25):
            if self.color_change_time == 0:
                self.color_change_time = self.powerup_time // (POWERUPTIME * 2)

                if (self.color_change_time < FPS // 10):
                    self.color_change_time = FPS // 10

                if self.cur_design == self.color:
                    self.setDesign(self.velocity, "BLUE")
                else:
                    self.setDesign(self.velocity, self.color)

            self.color_change_time -= 1


# --------------------------------------------------------------------------- #

class Booster(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "BOOST"
        self.powerups_remaining = PLAYERLIVES
        self.speed = abs(velocity)

        super().__init__(color, start_pos, velocity)

    # --- Setters --- #

    def setVelocity(self, velocity):
        if (self.velocity == velocity):
            super().setDesign(velocity, self.color)
        else:
            self.setImage(velocity, self.cur_design)

        self.velocity = (sign(velocity[0]) * self.speed, sign(velocity[1]) * self.speed)
        self.newTrail()

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail

        if self.powerup_active:
            self.activeTrail = BoostTrail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)
        else:
            self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS

            self.speed = abs(int(self.init_velocity * SPEEDBOOSTFACTOR))
            self.setVelocity(self.velocity)

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()

            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.speed = abs(self.init_velocity)

            self.setVelocity(self.velocity)

    # --- Other --- #

    def reset(self):
        self.speed = abs(self.init_velocity)

        super().reset()

# --------------------------------------------------------------------------- #

class Invisible(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "INVISIBLE"
        self.powerups_remaining = PLAYERLIVES

        super().__init__(color, start_pos, velocity)

    # --- Setters --- #

    def setVelocity(self, velocity):
        # Set image and color if powerup is active
        self.setImage(velocity, self.cur_design)
        self.velocity = velocity

        if not self.powerup_active:
            self.newTrail()

    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS
            self.invulnerable = True

            # Invisiblity Bike Color
            self.setDesign(self.velocity, "BLUE")

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()

            self.powerup_time -= 1

        else:   # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False
            self.invulnerable = False

            self.newTrail()
            self.setDesign(self.velocity, self.color)


# --------------------------------------------------------------------------- #

class Builder(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "WALL"
        self.powerups_remaining = PLAYERLIVES

        super().__init__(color, start_pos, velocity)

    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS

            self.newWall()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time -= 1
            self.wall.update()
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False

            self.newTrail()


    def newWall(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Wall(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y), trailSize)
        self.wall = self.activeTrail

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (self.activeTrail is not None) and (not isinstance(self.activeTrail, Wall)):
            self.activeTrail.update()

        if self.powerup_active:
            self.check_powerup()


# --------------------------------------------------------------------------- #

class Jumper(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "Jumper"
        self.powerups_remaining = PLAYERLIVES

        self.in_jump = False

        super().__init__(color, start_pos, velocity)

    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False:
            self.powerup_active = True
            self.powerup_time = POWERUPTIME * FPS

            self.setDesign(self.velocity, "BLUE")

        self.jump()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False
            self.setDesign(self.velocity, self.color)


    def check_jump(self):
        if (self.jump_time_remaining > 0):
            self.jump_time_remaining -= 1
        else:
            self.in_jump = False
            self.invulnerable = False
            self.newTrail()

    def jump(self):
        if not self.in_jump:
            self.in_jump = True
            self.invulnerable = True
            self.jump_time_remaining = JUMPTIME * FPS

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

    # --- Setters --- #

    def setVelocity(self, velocity):
        # Cant change velocity mid-jump
        if not self.in_jump:
            super().setVelocity(velocity)

    def update(self):
        super().update()

        if self.in_jump:
            self.check_jump()






