from pygame import mixer


class SoundPlayer(object):

    def __init__(self):
        mixer.pre_init(44100, 16, 2, 4096)

        self.theme_song = mixer.music.load("resources/audio/lightbike_theme_song.wav")

        self.menu_highlight = mixer.Sound("resources/audio/menu_select.wav")
        self.menu_action = mixer.Sound("resources/audio/menu_validate.wav")
        self.menu_continue = mixer.Sound("resources/audio/menu_continue.wav")

        self.round_start = mixer.Sound("resources/audio/round_start.wav")
        self.round_reset = mixer.Sound("resources/audio/round_reset.wav")
        self.game_over = mixer.Sound("resources/audio/game_over.wav")
        self.crash = mixer.Sound("resources/audio/crash.wav")

        self.boost = mixer.Sound("resources/audio/boost.wav")
        self.jump = mixer.Sound("resources/audio/jump.wav")
        self.ghost = mixer.Sound("resources/audio/ghost.wav")
        self.wall = mixer.Sound("resources/audio/wall.wav")

        self.menu_highlight.set_volume(0.5)
        self.menu_action.set_volume(0.6)
        self.menu_continue.set_volume(0.5)
        self.round_start.set_volume(0.4)
        self.game_over.set_volume(0.25)
        self.crash.set_volume(0.2)
        self.boost.set_volume(0.15)
        self.jump.set_volume(0.25)
        self.ghost.set_volume(0.5)
        self.wall.set_volume(0.15)

        self.sounds_list = [self.menu_highlight, self.menu_action, self.menu_continue, self.round_start,
                            self.round_reset, self.game_over, self.crash,
                            self.boost, self.jump, self.ghost, self.wall]


    def play_theme_song(self):
        mixer.music.stop()
        # self.theme_song = mixer.music.load("resources/audio/lightbike_theme_song.wav")
        mixer.music.play(-1)

    def pause_theme_song(self):
        mixer.music.pause()

    def unpause_theme_song(self):
        mixer.music.play()


    def play_menu_highlight(self):
        mixer.Sound.play(self.menu_highlight)

    def play_menu_action(self):
        mixer.Sound.play(self.menu_action)

    def play_menu_continue(self):
        mixer.Sound.play(self.menu_continue)


    def play_round_reset(self):
        mixer.Sound.play(self.round_reset)

    def play_round_start(self):
        mixer.Sound.stop(self.round_reset)
        mixer.Sound.play(self.round_start)

    def play_game_over(self):
        mixer.music.stop()
        self.stop_all_sounds()

        mixer.Sound.play(self.game_over)

    def play_crash(self):
        self.stop_all_sounds()

        mixer.Sound.play(self.crash)

    def play_boost(self):
        mixer.Sound.play(self.boost)

    def play_jump(self):
        mixer.Sound.play(self.jump)

    def play_ghost(self):
        mixer.Sound.play(self.ghost)

    def play_wall(self):
        mixer.Sound.play(self.wall)

    def stop_all_sounds(self):
        for sound in self.sounds_list:
            mixer.Sound.stop(sound)