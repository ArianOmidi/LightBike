from Game import *


class Menu(object):

    # Create all our attributes and initialize the game.
    def __init__(self):
        self.intro_screen = True
        self.instructions = False
        self.player_select = False
        self.game_started = False

        self.player_color_list = []
        self.player_selection_font = font.Font("../resources/fonts/retronoid.ttf", 60)
        self.bike_text_font = font.Font("../resources/fonts/retronoid.ttf", 40)

        self.bike_text_font.get_height()

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
                    elif event.key == pygame.K_SPACE:
                        self.intro_screen = False
                        self.instructions = True
                elif self.instructions:
                    if event.key == pygame.K_RETURN:
                        self.instructions = False
                        self.intro_screen = True
                elif self.player_select and len(self.player_color_list) == NUM_OF_PLAYERS:
                    if event.key == pygame.K_RETURN:
                        self.player_select = False
                        self.game_started = True

            # Player Select
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_select:
                    mouse_on_color = self.mouse_in_color()

                    if mouse_on_color != None and len(self.player_color_list) < NUM_OF_PLAYERS:
                        self.player_color_list.append(mouse_on_color)

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
            screen.blit(PLAYER_SELECT_SCREEN, (0, 0))

            player_one_text_color = player_two_text_color = DARK_TEXT_COLOR

            if len(self.player_color_list) == 0:
                player_one_text_color = TEXT_COLOR
            elif len(self.player_color_list) == 1:
                player_two_text_color = TEXT_COLOR

            player_one_text = self.player_selection_font.render("PLAYER 1", True, player_one_text_color)
            screen.blit(player_one_text, (80, 65))
            player_two_text = self.player_selection_font.render("PLAYER 2", True, player_two_text_color)
            screen.blit(player_two_text, (80, 3 * 60 + 10 * PLAYER_WIDTH))

            self.bike_pos = [
                (SCREEN_WIDTH - 60 * PLAYER_WIDTH, SCREEN_HEIGHT // 2 - 20 * PLAYER_WIDTH),
                (SCREEN_WIDTH - 30 * PLAYER_WIDTH, SCREEN_HEIGHT // 2 - 20 * PLAYER_WIDTH),
                (SCREEN_WIDTH - 60 * PLAYER_WIDTH, SCREEN_HEIGHT // 2),
                (SCREEN_WIDTH - 30 * PLAYER_WIDTH, SCREEN_HEIGHT // 2)
            ]

            mouse_on_color = self.mouse_in_color()

            image = Surface((20 * PLAYER_WIDTH + 2 * PLAYER_SELECT_OFFSET,
                             10 * PLAYER_WIDTH + 2 * PLAYER_SELECT_OFFSET + self.bike_text_font.get_height()))
            image.fill(DARK_TEXT_COLOR)

            if mouse_on_color != None:
                screen.blit(image, (self.bike_pos[getColorIndex(mouse_on_color)][0] - PLAYER_SELECT_OFFSET,
                                    self.bike_pos[getColorIndex(mouse_on_color)][
                                        1] - PLAYER_SELECT_OFFSET - self.bike_text_font.get_height()))

            for i in range(4):
                if not self.player_color_list.__contains__(getColor(i)):
                    bike_text = self.bike_text_font.render(getName(i), True, getTrailColor(getColor(i), None))
                    textRect = bike_text.get_rect()
                    textRect.center = (self.bike_pos[i][0] + 10 * PLAYER_WIDTH, self.bike_pos[i][1] - 35)

                    screen.blit(bike_text, textRect)

                    screen.blit(getPlayerSelectionBike(getColor(i), 1), self.bike_pos[i])
                elif self.player_color_list[0] == getColor(i):
                    screen.blit(getPlayerSelectionBike(getColor(i), 1), (80, self.bike_pos[0][1]))
                elif self.player_color_list[1] == getColor(i):
                    screen.blit(getPlayerSelectionBike(getColor(i), 1), (80, self.bike_pos[2][1]))

        pygame.display.update()

    def mouse_in_color(self):
        # mouse position
        mouse = pygame.mouse.get_pos()

        if not self.player_color_list.__contains__("RED") and self.bike_pos[0][0] - PLAYER_SELECT_OFFSET <= mouse[0] <= \
                self.bike_pos[0][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[0][
            1] - PLAYER_SELECT_OFFSET - self.bike_text_font.get_height() <= mouse[1] <= self.bike_pos[0][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "RED"
        elif not self.player_color_list.__contains__("BLUE") and self.bike_pos[1][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[1][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[1][
            1] - PLAYER_SELECT_OFFSET - self.bike_text_font.get_height() <= mouse[1] <= self.bike_pos[1][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "BLUE"
        elif not self.player_color_list.__contains__("YELLOW") and self.bike_pos[2][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[2][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[2][
            1] - PLAYER_SELECT_OFFSET - self.bike_text_font.get_height() <= mouse[1] <= self.bike_pos[2][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "YELLOW"
        elif not self.player_color_list.__contains__("GREEN") and self.bike_pos[3][0] - PLAYER_SELECT_OFFSET <= mouse[
            0] <= self.bike_pos[3][0] + 20 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET and self.bike_pos[3][
            1] - PLAYER_SELECT_OFFSET - self.bike_text_font.get_height() <= mouse[1] <= self.bike_pos[3][
            1] + 10 * PLAYER_WIDTH + PLAYER_SELECT_OFFSET:
            return "GREEN"
        else:
            return None

    def return_to_player_selection(self):
        self.player_select = True
        self.game_started = False

        self.player_color_list = []
