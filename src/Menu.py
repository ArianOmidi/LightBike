from Util import *
import pygame


class Menu(object):

    # Create all our attributes and initialize the game.
    def __init__(self,):
        self.intro_screen = True
        self.instructions = False
        self.player_select = False
        self.powerup_select = False
        self.game_started = False

        self.prev_mouse_index = -1

        self.player_color_list = []
        self.player_powerup_list = []
        self.player_attributes = []

        self.title_font = font.Font("resources/fonts/retronoid.ttf", 65)
        self.header_font = font.Font("resources/fonts/retronoid.ttf", 55)
        self.body_font = font.Font("resources/fonts/retronoid.ttf", 40)

        SOUND_PLAYER.play_theme_song()

    # --- RESET FUNCTION --- #

    def return_to_player_selection(self):
        self.player_select = True
        self.game_started = False

        self.player_color_list = []
        self.player_powerup_list = []

        SOUND_PLAYER.play_menu_continue()
        SOUND_PLAYER.play_theme_song()


    # --- EVENT CONTROLLER --- #

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:

                if self.intro_screen:
                    if event.key == pygame.K_RETURN:
                        self.intro_screen = False
                        self.player_select = True

                        SOUND_PLAYER.play_menu_continue()
                    elif event.key == pygame.K_SPACE:
                        self.intro_screen = False
                        self.instructions = True

                        SOUND_PLAYER.play_menu_continue()
                elif self.instructions:
                    if event.key == pygame.K_RETURN:
                        self.instructions = False
                        self.intro_screen = True

                        SOUND_PLAYER.play_menu_continue()
                elif self.player_select and len(self.player_color_list) == NUM_OF_PLAYERS:
                    if event.key == pygame.K_RETURN:
                        self.player_select = False
                        self.powerup_select = True

                        SOUND_PLAYER.play_menu_continue()
                elif self.powerup_select and len(self.player_powerup_list) == NUM_OF_PLAYERS:
                    if event.key == pygame.K_RETURN:
                        self.powerup_select = False
                        self.game_started = True

                        self.player_attributes = [[self.player_color_list[0], self.player_powerup_list[0]],
                                                  [self.player_color_list[1], self.player_powerup_list[1]]]

                        SOUND_PLAYER.play_menu_continue()

            # Player Select
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_select:
                    mouse_on_color = self.mouse_in_color()

                    if mouse_on_color != None and len(self.player_color_list) < NUM_OF_PLAYERS:
                        self.player_color_list.append(mouse_on_color)
                        SOUND_PLAYER.play_menu_action()
                elif self.powerup_select:
                    mouse_on_powerup = self.mouse_on_powerup()

                    if mouse_on_powerup != None and len(self.player_powerup_list) < NUM_OF_PLAYERS:
                        self.player_powerup_list.append(mouse_on_powerup)
                        SOUND_PLAYER.play_menu_action()


        return False


    # --- DRAWING --- #

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BACKGROUND)

        if self.intro_screen:
            screen.blit(INTRO_SCREEN, (0, 0))
        elif self.intro_screen:
            screen.blit(INSTRUCTION_SCREEN, (0, 0))
        elif self.player_select:
            # Set Background
            screen.blit(PLAYER_SELECT_SCREEN, (0, 0))

            # Draw Screen Text
            if len(self.player_color_list) == NUM_OF_PLAYERS:
                title_text = self.title_font.render("SELECT BIKE", True, DARK_TEXT_COLOR)
                continue_text = self.body_font.render("PRESS ENTER TO CONTINUE...", True, TEXT_COLOR)

                screen.blit(continue_text,
                            (SCREEN_WIDTH - continue_text.get_width(), SCREEN_HEIGHT - continue_text.get_height()))
            else:
                title_text = self.title_font.render("SELECT BIKE", True, TEXT_COLOR)

            screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 5))

            """ Set Player Text and Bikes """
            player_one_text_color = player_two_text_color = DARK_TEXT_COLOR

            if len(self.player_color_list) == 0:
                player_one_text_color = TEXT_COLOR
            elif len(self.player_color_list) == 1:
                player_two_text_color = TEXT_COLOR

            # Draw Player Text
            player_one_text = self.header_font.render("PLAYER 1", True, player_one_text_color)
            screen.blit(player_one_text, (80, 75))
            player_two_text = self.header_font.render("PLAYER 2", True, player_two_text_color)
            screen.blit(player_two_text, (80, 3 * 60 + 10 * PLAYER_WIDTH + 10))

            self.bike_pos = [
                (SCREEN_WIDTH - 60 * PLAYER_WIDTH, SCREEN_HEIGHT // 2 - 20 * PLAYER_WIDTH),
                (SCREEN_WIDTH - 30 * PLAYER_WIDTH, SCREEN_HEIGHT // 2 - 20 * PLAYER_WIDTH),
                (SCREEN_WIDTH - 60 * PLAYER_WIDTH, SCREEN_HEIGHT // 2),
                (SCREEN_WIDTH - 30 * PLAYER_WIDTH, SCREEN_HEIGHT // 2)
            ]

            mouse_on_color = self.mouse_in_color()

            image = Surface((20 * PLAYER_WIDTH + 2 * PLAYER_SELECT_OFFSET,
                             10 * PLAYER_WIDTH + 2 * PLAYER_SELECT_OFFSET))
            image.fill(DARK_TEXT_COLOR)

            if mouse_on_color != None:
                if self.prev_mouse_index != getColorIndex(mouse_on_color):
                    SOUND_PLAYER.play_menu_highlight()

                screen.blit(image, (self.bike_pos[getColorIndex(mouse_on_color)][0] - PLAYER_SELECT_OFFSET,
                                    self.bike_pos[getColorIndex(mouse_on_color)][
                                        1] - PLAYER_SELECT_OFFSET))

            self.prev_mouse_index = getColorIndex(mouse_on_color)

            for i in range(4):
                if not self.player_color_list.__contains__(getColor(i)):
                    screen.blit(getPlayerSelectionBike(getColor(i), 1), self.bike_pos[i])
                elif self.player_color_list[0] == getColor(i):
                    screen.blit(getPlayerSelectionBike(getColor(i), 1), (80, self.bike_pos[0][1]))
                elif self.player_color_list[1] == getColor(i):
                    screen.blit(getPlayerSelectionBike(getColor(i), 1), (80, self.bike_pos[2][1]))

        elif self.powerup_select:
            # Set Background
            screen.blit(PLAYER_SELECT_SCREEN, (0, 0))

            # Draw Screen Text
            if len(self.player_powerup_list) == NUM_OF_PLAYERS:
                title_text = self.title_font.render("SELECT BIKE", True, DARK_TEXT_COLOR)
                continue_text = self.body_font.render("PRESS ENTER TO START GAME...", True, TEXT_COLOR)

                screen.blit(continue_text,
                            (SCREEN_WIDTH - continue_text.get_width(), SCREEN_HEIGHT - continue_text.get_height()))
            else:
                title_text = self.title_font.render("SELECT POWERUP", True, TEXT_COLOR)

            screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 5))

            """ Set Player Text and Bikes """
            player_one_text_color = player_two_text_color = DARK_TEXT_COLOR

            # Let the player choosing have a white colored text
            if len(self.player_powerup_list) == 0:
                player_one_text_color = TEXT_COLOR
            elif len(self.player_powerup_list) == 1:
                player_two_text_color = TEXT_COLOR

            # Draw Player Text
            player_one_text = self.header_font.render("PLAYER 1", True, player_one_text_color)
            screen.blit(player_one_text, (80, 75))
            player_two_text = self.header_font.render("PLAYER 2", True, player_two_text_color)
            screen.blit(player_two_text, (80, 3 * 60 + 10 * PLAYER_WIDTH + 10))

            # Draw Selected Bikes
            screen.blit(getPlayerSelectionBike(self.player_color_list[0], 1), (80, self.bike_pos[0][1]))
            screen.blit(getPlayerSelectionBike(self.player_color_list[1], 1), (80, self.bike_pos[2][1]))

            """ Set Position of Powerup Icons """
            self.powerup_pos = [
                (SCREEN_WIDTH - 7 * POWERUP_SELECTION_ICON_SIZE // 2, self.bike_pos[0][1] - 20),
                (SCREEN_WIDTH - 2 * POWERUP_SELECTION_ICON_SIZE, self.bike_pos[0][1] - 20),
                (SCREEN_WIDTH - 7 * POWERUP_SELECTION_ICON_SIZE // 2, self.bike_pos[2][1] - 20),
                (SCREEN_WIDTH - 2 * POWERUP_SELECTION_ICON_SIZE, self.bike_pos[2][1] - 20)
            ]

            mouse_on_powerup = self.mouse_on_powerup()

            image = Surface((POWERUP_SELECTION_ICON_SIZE + 2 * PLAYER_SELECT_OFFSET,
                             POWERUP_SELECTION_ICON_SIZE + 2 * PLAYER_SELECT_OFFSET))
            image.fill(DARK_TEXT_COLOR)

            if mouse_on_powerup != None:
                if self.prev_mouse_index != getPowerupIndex(mouse_on_powerup):
                    SOUND_PLAYER.play_menu_highlight()

                screen.blit(image, (self.powerup_pos[getPowerupIndex(mouse_on_powerup)][0] - PLAYER_SELECT_OFFSET,
                                    self.powerup_pos[getPowerupIndex(mouse_on_powerup)][
                                        1] - PLAYER_SELECT_OFFSET))

            self.prev_mouse_index = getPowerupIndex(mouse_on_powerup)

            for i in range(4):
                screen.blit(getPowerupSelectionIcon(getPowerup(i)), self.powerup_pos[i])

                if len(self.player_powerup_list) >= 1:
                    screen.blit(getPowerupSelectionIcon(self.player_powerup_list[0]),
                                (80 + 20 * PLAYER_WIDTH + 40, self.powerup_pos[0][1]))
                if len(self.player_powerup_list) >= 2:
                    screen.blit(getPowerupSelectionIcon(self.player_powerup_list[1]),
                                (80 + 20 * PLAYER_WIDTH + 40, self.powerup_pos[2][1]))


        pygame.display.update()


     # --- MOUSE POSITION FUNCTIONS --- #

    def mouse_in_color(self):
        # mouse position
        mouse = pygame.mouse.get_pos()

        if not self.player_color_list.__contains__("RED") and self.bike_pos[0][0] - PLAYER_SELECT_OFFSET <= mouse[0] <= \
                self.bike_pos[0][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[0][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.bike_pos[0][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "RED"
        elif not self.player_color_list.__contains__("BLUE") and self.bike_pos[1][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[1][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[1][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.bike_pos[1][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "BLUE"
        elif not self.player_color_list.__contains__("YELLOW") and self.bike_pos[2][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[2][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[2][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.bike_pos[2][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "YELLOW"
        elif not self.player_color_list.__contains__("GREEN") and self.bike_pos[3][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[3][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[3][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.bike_pos[3][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "GREEN"
        else:
            return None

    def mouse_on_powerup(self):
        # mouse position
        mouse = pygame.mouse.get_pos()

        if self.powerup_pos[0][0] - PLAYER_SELECT_OFFSET <= \
                mouse[0] <= \
                self.powerup_pos[0][0] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET and self.powerup_pos[0][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.powerup_pos[0][
            1] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET:
            return getPowerup(0)
        elif self.powerup_pos[1][
            0] - PLAYER_SELECT_OFFSET <= mouse[0] <= \
                self.powerup_pos[1][0] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET and self.powerup_pos[1][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.powerup_pos[1][
            1] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET:
            return getPowerup(1)
        elif self.powerup_pos[2][
            0] - PLAYER_SELECT_OFFSET <= mouse[0] <= \
                self.powerup_pos[2][0] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET and self.powerup_pos[2][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.powerup_pos[2][
            1] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET:
            return getPowerup(2)
        elif self.powerup_pos[3][
            0] - PLAYER_SELECT_OFFSET <= mouse[0] <= \
                self.powerup_pos[3][0] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET and self.powerup_pos[3][
            1] - PLAYER_SELECT_OFFSET <= mouse[1] <= self.powerup_pos[3][
            1] + POWERUP_SELECTION_ICON_SIZE + PLAYER_SELECT_OFFSET:
            return getPowerup(3)
        else:
            return None



