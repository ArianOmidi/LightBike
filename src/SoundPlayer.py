from pygame import mixer


class SoundPlayer(object):

    def __init__(self):
        mixer.pre_init(44100, 16, 2, 4096)

        self.theme_song = mixer.music.load("../resources/audio/lightbike_theme_song.wav")
        self.countdown = mixer.Sound("../resources/audio/countdown.wav")
        self.menu_highlight = mixer.Sound("../resources/audio/menu_highlight.wav")
        self.menu_action = mixer.Sound("../resources/audio/menu_action.wav")
        self.round_start = mixer.Sound("../resources/audio/game_start.wav")
        self.game_over = mixer.Sound("../resources/audio/game_over.wav")
        self.explosion = mixer.Sound("../resources/audio/explosion.wav")

        self.boost = mixer.Sound("../resources/audio/boost.wav")

        self.menu_highlight.set_volume(0.2)
        self.game_over.set_volume(0.35)
        self.explosion.set_volume(0.25)
        self.boost.set_volume(0.25)

        self.countdown_playing = False

    def play_theme_song(self):
        mixer.music.stop()
        # self.theme_song = mixer.music.load("../resources/audio/lightbike_theme_song.wav")
        mixer.music.play(-1)

    def pause_theme_song(self):
        mixer.music.pause()

    def unpause_theme_song(self):
        mixer.music.play()

    def play_countdown(self):
        if not self.countdown_playing:
            self.pause_theme_song()
            mixer.Sound.play(self.countdown)
            self.countdown_playing = True

    def play_menu_highlight(self):
        mixer.Sound.play(self.menu_highlight)

    def play_menu_action(self):
        mixer.Sound.play(self.menu_action)

    def play_round_start(self):
        mixer.Sound.play(self.round_start)

    def play_game_over(self):
        mixer.music.stop()
        mixer.Sound.play(self.game_over)

    def play_explosion(self):
        # mixer.music.stop()
        mixer.Sound.play(self.explosion)

    def play_boost(self):
        mixer.Sound.play(self.boost)
