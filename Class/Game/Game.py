from Pokemon import Pokemon  # Pokemon class
from Combat import Combat  # Combat class
from Player import Player  # Player class
from Settings import *  # Settings class


class Game:
    def __init__(self):
        # Init pygame #
        pg.init()

        # Init settings #
        self.SETTINGS = Settings()  # Settings class

        # init screen #
        pg.display.set_caption("Pokemon")
        self.screen = pg.display.set_mode(self.SETTINGS.WIN_RES)
        self.clock = pg.time.Clock()

        # Init classes #
        self.GAME = self  # Game class
        self.COLORS = Colors()  # Colors class
        self.SPRITES = Sprites()  # Sprites class
        self.GENERATE = Generate()  # Generate class
        self.Player = Player()  # Player class

        # Game variables #
        self.game_state = "menu"  # Game state (menu, combat, etc)
        self.menu_state = "main"  # Menu state (main, pokemon, etc)
        self.COMBAT = None  # Combat class

        # time #
        self.last_time = pg.time.get_ticks()
        self.current_time = 0

        # Debug #
        self.Debug()

    # Start combat function #
    def start_combat(self, pokemon, enemy):
        self.COMBAT = Combat(self.GAME, pokemon, enemy)
        self.game_state = "combat"

    # Debug function (for testing) don't forget to remove it before release #
    def Debug(self):

        print("Debug")

        # Debug Add pokemon
        self.Player.add_pokemons(Pokemon(self, 4, self.GENERATE.generate_IV(), 20, self.GENERATE.generate_nature(), 5, [1, 3, 39], False))
        self.Player.get_pokemons()[0].set_exp(25)
        # self.Player.add_pokemons(Pokemon(self, 5, self.GENERATE.generate_IV(), 1, self.GENERATE.generate_nature(), 1, [1, 3, 6, 4], True))

        # Debug Level up pokemon
        # for i in range(1, 10):
        #     self.Player.get_pokemons()[0].level_up()

        # Debug Combat
        self.start_combat(self.Player.get_pokemons(), Pokemon(self, 1, self.GENERATE.generate_IV(), 1, self.GENERATE.generate_nature(), 5, [1], False))

    # Pygame Draw function #
    def draw(self):
        if self.game_state == "map":
            self.screen.fill(self.COLORS.BLACK)
            # INDEV WATERMARK #
            self.SETTINGS.combat_font.render_to(self.screen, (1150, 10), "INDEV", self.COLORS.WHITE, size=50)

        if self.game_state == "combat":
            self.COMBAT.draw(self.screen)
            # INDEV WATERMARK #
            self.SETTINGS.combat_font.render_to(self.screen, (1150, 10), "INDEV", self.COLORS.BLACK, size=50)



        pg.display.flip()
        pg.display.update()

    def input(self, event):
        if self.game_state == "combat":
            self.COMBAT.input(event)
        elif self.game_state == "map":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.start_combat(self.Player.get_pokemons(), Pokemon(self, 1, self.GENERATE.generate_IV(), 1, self.GENERATE.generate_nature(), 5, [1], False))

    # GAME LOOP #
    def run(self):
        while True:
            self.current_time = pg.time.get_ticks()
            self.clock.tick(self.SETTINGS.FPS)
            self.draw()
            for event in pg.event.get():
                self.input(event)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()


# Create the game instance #
game = Game()
game.run()

