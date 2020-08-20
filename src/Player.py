from Trail import *

class Player(pygame.sprite.Sprite):

    def __init__(self, color, start_pos, velocity):
        # Call parent class constructor
        super().__init__()

        # Variables
        self.color = color
        self.lives = PLAYER_LIVES

        # Powerup Variables
        self.powerup_active = False
        self.invulnerable = False
        self.color_change_time = 0

        # Set Velocity and Position
        self.init_velocity = velocity
        self.init_pos = start_pos
        self.velocity = (velocity, 0)

        # Sets Image (orientation and color of the bike)
        self.setImage(self.velocity, self.color)

        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]

        # Sets Trail
        self.activeTrail = None
        self.newTrail()




    # --- Setters --- #

    # Sets design and changes rectangle pos if bike is moving in a different dir
    def setImage(self, new_vel, color):
        self.cur_design = color
        self.image = getBike(new_vel, color)

        if getUnitVector(self.velocity) != getUnitVector(new_vel):
            change_x = change_y = 0
            old_pos = (self.rect.x, self.rect.y)

            if (new_vel[0] != 0):
                if (new_vel[0] < 0):
                    change_x -= PLAYER_WIDTH

                if (self.velocity[1] > 0):
                    change_y += PLAYER_WIDTH
            else:
                if (new_vel[1] < 0):
                    change_y -= PLAYER_WIDTH

                if (self.velocity[0] > 0):
                    change_x += PLAYER_WIDTH

            self.rect = self.image.get_rect()
            self.rect.x = old_pos[0] + change_x
            self.rect.y = old_pos[1] + change_y

    # Set new velocity
    def setVelocity(self, velocity):
        """ Change the speed of the player"""
        self.setImage(velocity, self.cur_design)
        self.velocity = velocity
        self.newTrail()

    # Set new trail
    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))

    # --- Powerup Classes --- #

    # def powerup(self):

    # def check_powerup(self):

    def powerup_time_warning(self):
        # Change Bike color to inform player that the powerup is running out
        # Color changes faster when there is less time
        if (self.powerup_time < BOOSTER_POWERUP_TIME * FPS / 1.75):
            if self.color_change_time == 0:
                self.color_change_time = self.powerup_time // (BOOSTER_POWERUP_TIME * 2)

                if (self.color_change_time < FPS // 10):
                    self.color_change_time = FPS // 10

                if self.cur_design == self.color:
                    self.setImage(self.velocity, "POWERUP_" + self.color)
                else:
                    self.setImage(self.velocity, self.color)

            self.color_change_time -= 1


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
        self.velocity = (self.init_velocity, 0)
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.cur_design = self.color

        self.image = getBike(self.velocity, self.color)

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




# --------------------------------------------------------------------------- #

class Booster(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "BOOSTER"
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.speed = abs(velocity)

        super().__init__(color, start_pos, velocity)

    # --- Setters --- #

    def setVelocity(self, velocity):
        super().setVelocity((sign(velocity[0]) * self.speed, sign(velocity[1]) * self.speed))

    def newTrail(self):
        if self.activeTrail != None:
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail

        if self.powerup_active:
            self.activeTrail = BoostTrail(self, getTrailColor(self.color, self.powerup_active),
                                          (self.rect.x, self.rect.y))
        else:
            self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = BOOSTER_POWERUP_TIME * FPS

            self.speed = abs(int(self.init_velocity * SPEED_BOOST_FACTOR))
            self.setVelocity(self.velocity)

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:
            self.powerup_active = False
            self.speed = abs(self.init_velocity)
            self.cur_design = self.color

            self.setVelocity(self.velocity)

    # --- Other --- #

    def reset(self):
        self.speed = abs(self.init_velocity)

        super().reset()

# --------------------------------------------------------------------------- #

class Invisible(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "INVISIBLE"
        self.powerups_remaining = getNumOfPowerups(self.power)

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
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = INVISIBLE_POWERUP_TIME * FPS
            self.invulnerable = True

            # Invisiblity Bike Color
            self.setImage(self.velocity, "POWERUP_" + self.color)

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
            self.setImage(self.velocity, self.color)


# --------------------------------------------------------------------------- #

# todo glitch with builder not making wall when 2 buttons pressed
class Builder(Player):
    def __init__(self, color, start_pos, velocity):
        self.power = "BUILDER"
        self.powerups_remaining = getNumOfPowerups(self.power)

        self.new_wall_made = False
        self.deleted_trail = None

        super().__init__(color, start_pos, velocity)


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = BUILDER_POWERUP_TIME * FPS

            self.newWall()

    def check_powerup(self):
        if (self.powerup_time > 0 and self.wall.update()):
            self.powerup_time -= 1
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False


    def newWall(self):
        self.new_wall_made = True
        self.deleted_trail = self.activeTrail

        self.wall = Wall(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y),
                         self.deleted_trail)
        self.activeTrail = self.wall

    # --- Setters --- #

    def newTrail(self):
        self.new_wall_made = False

        if self.activeTrail != None and not isinstance(self.activeTrail, Wall):
            self.activeTrail.endTrail()
        self.lastActiveTrail = self.activeTrail
        self.activeTrail = Trail(self, getTrailColor(self.color, self.powerup_active), (self.rect.x, self.rect.y))

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
        self.power = "JUMPER"
        self.powerups_remaining = getNumOfPowerups(self.power)
        self.in_jump = False

        super().__init__(color, start_pos, velocity)


    # --- Powerup Functions --- #

    def powerup(self):
        if self.powerup_active == False and self.powerups_remaining > 0:
            self.powerups_remaining -= 1
            self.powerup_active = True
            self.powerup_time = JUMPER_POWERUP_TIME * FPS

        self.jump()

    def check_powerup(self):
        if (self.powerup_time > 0):
            self.powerup_time_warning()
            self.powerup_time -= 1
        else:  # If powerup time is over turn off invisibility and set regular design
            self.powerup_active = False
            self.setImage(self.velocity, self.color)

    def jump(self):
        if not self.in_jump:
            self.in_jump = True
            self.invulnerable = True
            self.jump_time_remaining = JUMP_TIME * FPS

            # End Trail
            self.activeTrail.endTrail()
            self.lastActiveTrail = self.activeTrail
            self.activeTrail = None

    def check_jump(self):
        if (self.jump_time_remaining > 0):
            self.jump_time_remaining -= 1
        else:
            self.in_jump = False
            self.invulnerable = False
            self.newTrail()


    # --- Setters --- #

    def setVelocity(self, velocity):
        # Cant change velocity mid-jump
        if not self.in_jump:
            super().setVelocity(velocity)

    def update(self):
        super().update()

        if self.in_jump:
            self.check_jump()






