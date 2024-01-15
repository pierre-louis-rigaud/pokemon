import json
import random
import pygame as pg
import pygame.freetype as ft
import sys


class Settings:
    def __init__(self):
        # Language settings #
        self.language = "english"

        # path to pokemon data #
        with open("../../Data/Pokemon/Pokedex.json", "r", encoding="utf8") as json_file:
            self.pokedex = json.load(json_file)

        # path to type chart #
        with open("../../Data/Pokemon/Type_chart.json", "r", encoding="utf8") as json_file:
            self.type_chart = json.load(json_file)

        # path to natures #
        with open("../../Data/Pokemon/Nature.json", "r", encoding="utf8") as json_file:
            self.natures = json.load(json_file)

        # path to moves #
        with open("../../Data/Pokemon/Moves.json", "r", encoding="utf8") as json_file:
            self.moves = json.load(json_file)

        # pygame settings #
        self.WIN_RES = (1280, 720)
        self.FPS = 60

        # Fonts #
        self.combat_font = ft.Font("../../Data/Game/Font/pokemon_fire_red.ttf", 32)


class Generate(Settings):

    # Generate IV(0-31) #
    def generate_IV(self):
        return random.randint(0, 31)

    # Generate EV(0-255) #
    def generate_EV(self):
        return random.randint(0, 255)

    # Generate Nature(shy, brave, etc) #
    def generate_nature(self):
        return random.choice(list(self.natures.keys()))

    # Generate Level(1-100) #
    def generate_lvl(self):
        return random.randint(1, 100)


class Colors:
    def __init__(self):
        # Colors #
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (255, 0, 255)
        self.CYAN = (0, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (192, 192, 192)
        self.DARK_GRAY = (64, 64, 64)
        self.BROWN = (128, 64, 0)
        self.ORANGE = (255, 128, 0)
        self.PINK = (255, 128, 128)
        self.LIGHT_BLUE = (128, 128, 255)
        self.LIGHT_GREEN = (128, 255, 128)
        self.LIGHT_YELLOW = (255, 255, 128)
        self.LIGHT_RED = (255, 128, 128)
        self.LIGHT_PURPLE = (255, 128, 255)
        self.LIGHT_CYAN = (128, 255, 255)


class Sprites(Colors):

    def __init__(self):
        super().__init__()
        # Combat Sprites #
        self.forest_background = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/Background/Forest_Background.png"), (1280, 500))
        self.desert_background = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/Background/Desert_Background.png"), (1280, 500))
        self.lake_background = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/Background/Lake_Background.png"), (1280, 500))
        self.sea_background = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/Background/Sea_Background.png"), (1280, 500))
        self.training_background = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/Background/Training_Background.png"), (1280, 500))

        # UI Sprites #
        self.bottom_message_box = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Bottom_Message_Box.png"), (1280, 220))
        self.choice_box = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Choice_Box.png"), (600, 220))
        self.choice_arrow = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Choice_Arrow.png"), (40, 50))
        self.enemy_pokemon_status = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Enemy_Pokemon_Stats.png"), (500, 150))
        self.player_pokemon_status = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Player_Pokemon_Stats.png"), (500, 150))
        self.choice_move_box = pg.transform.scale(pg.image.load("../../Data/Combat/Combat_Sprite/CombatUI/Move_Box.png"), (1280, 220))

        # Animation Cooldown #
        self.player_intro_speed = 250

    def get_pokemon_sprite(self, pokemon_id, position):
        sprite = pg.image.load(f"../../Data/Pokemon/Pokemon_Sprites/{position}/{pokemon_id}.png").convert_alpha()
        return pg.transform.scale(sprite, (300, 300))

    def get_combat_player_sprite(self, id):
        sprite = pg.image.load(f"../../Data/Combat/Combat_Intro_Player/{id}.png")
        return pg.transform.scale(sprite, (sprite.get_width() * 6, sprite.get_height() * 6))
