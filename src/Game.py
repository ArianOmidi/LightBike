from Player import *
from PlayerIconBar import *
from Trail import *
from Util import *


class Game(object):

    # Create all our attributes and initialize the game.
    def __init__(self, player_attributes):
        self.round_timer = - 3 * FPS
        self.game_over = False
        self.round_in_progress = False
        self.menu_selected = False

        self.player_attributes = player_attributes

        # Create sprite lists
        self.trail_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()

        # Create the players
        self.player_one = self.set_player(player_attributes[0], 1)
        self.player_two = self.set_player(player_attributes[1], 2)

        self.player_list.add(self.player_one)
        self.player_list.add(self.player_two)

        self.player_one_icon_bar = PlayerIconBar(self.player_one, True)
        self.player_two_icon_bar = PlayerIconBar(self.player_two, False)

        # Add Borders
        self.add_borders()

        # Add Fonts
        init_fonts(self)

    def set_player(self, player_attributes, player_num):
        if player_num == 1:
            starting_pos = PLAYER_ONE_STARTING_POS
            starting_vel = VELOCITY
        elif player_num == 2:
            starting_pos = PLAYER_TWO_STARTING_POS
            starting_vel = -VELOCITY
        else:
            return None

        if player_attributes[1] == "BOOST":
            return Booster(player_attributes[0], starting_pos, starting_vel)
        elif player_attributes[1] == "GHOST":
            return Ghost(player_attributes[0], starting_pos, starting_vel)
        elif player_attributes[1] == "JUMP":
            return Jumper(player_attributes[0], starting_pos, starting_vel)
        elif player_attributes[1] == "WALL":
            return Builder(player_attributes[0], starting_pos, starting_vel)

    # --- EVENT CONTROLLER --- #

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:

                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__(self.player_attributes)
                    if event.key == pygame.K_RETURN:
                        self.menu_selected = True

                elif self.round_in_progress:
                    # Player One
                    if (self.player_one.velocity[0] == 0):
                        if event.key == pygame.K_a:
                            self.player_one.setVelocity((-VELOCITY, 0))
                        elif event.key == pygame.K_d:
                            self.player_one.setVelocity((VELOCITY, 0))
                    else:
                        if event.key == pygame.K_w:
                            self.player_one.setVelocity((0, -VELOCITY))
                        elif event.key == pygame.K_s:
                            self.player_one.setVelocity((0, VELOCITY))

                    if event.key == pygame.K_SPACE:
                        self.player_one.powerup()

                    # Player Two
                    if (self.player_two.velocity[0] == 0):
                        if event.key == pygame.K_LEFT:
                            self.player_two.setVelocity((-VELOCITY, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.player_two.setVelocity((VELOCITY, 0))
                    else:
                        if event.key == pygame.K_UP:
                            self.player_two.setVelocity((0, -VELOCITY))
                        elif event.key == pygame.K_DOWN:
                            self.player_two.setVelocity((0, VELOCITY))

                    if event.key == pygame.K_RETURN:
                        self.player_two.powerup()

        return False

    # --- GAME LOGIC --- #

    def run_logic(self):
        # This method is run each time through the frame. It
        # updates positions and checks for collisions.
        if self.game_over:
            return

        self.round_timer += 1

        if self.round_timer == 0:
            self.new_round()

        if self.round_in_progress:
            # Move the player
            self.player_list.update()

            for player in self.player_list:
                # Add any new trails
                if not (self.trail_list.__contains__(player.activeTrail) or player.activeTrail is None):
                    self.trail_list.add(player.activeTrail)

                # Check if player is in bounds
                if player.rect.x < BORDER_WIDTH or player.rect.x > SCREEN_WIDTH - BORDER_WIDTH - 2 * PLAYER_WIDTH or player.rect.y < BORDER_TOP_OFFSET + BORDER_WIDTH or player.rect.y > SCREEN_HEIGHT - BORDER_WIDTH - 2 * PLAYER_WIDTH:
                    self.game_over = player.death()

                    self.round_in_progress = False
                    self.round_timer = - 3 * FPS

                    if self.game_over:
                        break
                    else:
                        continue

                # FOR BUILDER ONLY: Delete old trail from list when wall is made
                if isinstance(player, Builder) and isinstance(player.activeTrail, Wall):
                    self.trail_list.remove(player.deleted_trail)

                # If player invulnerable skip over hit detection
                if player.invulnerable:
                    continue

                # --- COLLISIONS --- #

                # See if the player has collided with anything.
                trail_hit_list = pygame.sprite.spritecollide(player, self.trail_list, False)

                # Check the list of collisions.
                for trail in trail_hit_list:
                    if (trail == player.activeTrail or trail == player.lastActiveTrail):
                        continue

                    self.game_over = player.death()
                    self.round_in_progress = False
                    self.round_timer = - 3 * FPS

                    if self.game_over:
                        break
                    else:
                        continue
                    # You can do something with "block" here.

    # --- ROUND FUNCTIONS --- #

    def new_round(self):
        self.trail_list.empty()
        self.add_borders()

        for player in self.player_list:
            player.reset()
            self.trail_list.add(player.activeTrail)

        self.round_in_progress = True

    # --- DRAWING --- #

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        self.clear_screen(screen)

        # self.check_hitboxes(screen)
        self.trail_list.draw(screen)
        self.player_list.draw(screen)

        # ICON BAR
        screen.blit(self.player_one_icon_bar.getPlayerIconBar(), (BORDER_WIDTH + 60, BORDER_WIDTH))
        screen.blit(self.player_two_icon_bar.getPlayerIconBar(), (SCREEN_WIDTH // 2 - BORDER_WIDTH - 65, BORDER_WIDTH))
        blit_icon_bar(screen)

        # ROUND TEXT
        if self.game_over:
            gameover_text(self, screen)
        elif (self.round_timer < -2 * FPS):
            blit_text("3", "retronoid", 200, TEXT_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), screen)
        elif (self.round_timer < -FPS):
            blit_text("2", "retronoid", 200, TEXT_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), screen)
        elif (self.round_timer < 0):
            blit_text("1", "retronoid", 200, TEXT_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), screen)
        elif (self.round_timer < FPS):
            blit_text("GO", "retronoid", 200, TEXT_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), screen)

        pygame.display.update()

    def clear_screen(self, screen):
        screen.fill(BACKGROUND)

        for i in range(0, GRIDLINES):
            pygame.draw.line(screen, GRIDCOLOR,
                             [0, i * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2 + BORDER_TOP_OFFSET],
                             [SCREEN_WIDTH,
                              i * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2 + BORDER_TOP_OFFSET], 1)
        for j in range(0, GRIDLINES):
            pygame.draw.line(screen, GRIDCOLOR,
                             [j * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2, + BORDER_TOP_OFFSET],
                             [j * SCREEN_WIDTH / GRIDLINES + SCREEN_WIDTH / GRIDLINES / 2,
                              SCREEN_WIDTH + BORDER_TOP_OFFSET], 1)

        for i in range(0, GRIDLINES + 1):
            pygame.draw.line(screen, BACKGROUND, [0, i * SCREEN_WIDTH / GRIDLINES + BORDER_TOP_OFFSET],
                             [SCREEN_WIDTH, i * SCREEN_WIDTH / GRIDLINES + BORDER_TOP_OFFSET],
                             int(SCREEN_WIDTH / GRIDLINES / 6))
        for j in range(0, GRIDLINES + 1):
            pygame.draw.line(screen, BACKGROUND, [j * SCREEN_WIDTH / GRIDLINES, BORDER_TOP_OFFSET],
                             [j * SCREEN_WIDTH / GRIDLINES, SCREEN_WIDTH + BORDER_TOP_OFFSET],
                             int(SCREEN_WIDTH / GRIDLINES / 6))

        # Offset Fill
        offset_fill = pygame.Surface((SCREEN_WIDTH, BORDER_TOP_OFFSET))
        offset_fill.fill(GRIDCOLOR)

        screen.blit(offset_fill, (0, 0))

    def add_borders(self):
        # Create borders
        self.trail_list.add(Border((0, 0), (SCREEN_WIDTH, BORDER_WIDTH)))
        self.trail_list.add(Border((0, BORDER_TOP_OFFSET), (SCREEN_WIDTH, BORDER_WIDTH)))
        self.trail_list.add(Border((0, SCREEN_HEIGHT - BORDER_WIDTH), (SCREEN_WIDTH, BORDER_WIDTH)))
        self.trail_list.add(Border((0, 0), (BORDER_WIDTH, SCREEN_HEIGHT)))
        self.trail_list.add(Border((SCREEN_WIDTH - BORDER_WIDTH, 0), (BORDER_WIDTH, SCREEN_HEIGHT)))

    # --- TESTING --- #

    def check_hitboxes(self, screen):
        sprite_list = pygame.sprite.Group()

        for trail in self.trail_list:
            hitbox = Hitbox(trail)
            sprite_list.add(hitbox)

        for player in self.player_list:
            hitbox = Hitbox(player)
            sprite_list.add(hitbox)

        sprite_list.draw(screen)
