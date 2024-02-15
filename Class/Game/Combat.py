import random
import math

import pygame


class Combat:
    def __init__(self, game, player_pokemons, enemy_pokemon):
        self.game = game  # Game object
        self.__player_pokemon = player_pokemons[0]  # Pokemon object
        self.__enemy_pokemon = enemy_pokemon  # Enemy object
        self.__run_attempt = 0  # take note of the number of run attempt

        # Combat variables #
        self.__choice = 1  # choice of the player (depends on the menu)

        # Menu variables #
        self.__menu = 0  # menu state (0: menu_choices, 1: attack, 2: bag, 3: pokemon, 4: run)

        # Visuals Variables #
        self.__enemy_pokemon_x = 1280
        self.__player_sprite_x = -400
        self.__player_sprite = 1
        self.__pokemon_scale = 20
        self.__pokemon__y = 420
        self.__pokemon__x = 400
        self.__spawn_color = 200

        # Check who attack first
        self.attacker = self.check_who_attack_first()

        # save enemy turn state
        self.__enemy_attack_next_turn = False

        # last move
        self.__last_move = ""

        # Animation variables #
        self.__intro_played = False
        self.__enemy_pokemon_spawned = False
        self.__pokemon_spawned = False
        self.__player_pokemon_old_hp = self.__player_pokemon.get_hp()
        self.__enemy_pokemon_old_hp = self.__enemy_pokemon.get_hp()
        self.__player_animation_hp = False
        self.__enemy_animation_hp = False

        # self.turn()  # start the combat

    # ATTACK METHOD (return the damage)
    def attack(self, lvl, attack, attack_spe, attack_type, attack_category, power, enemy_defence, enemy_sp_defence, enemy_type):  # lvl(int), attack(int), attack_spe(int), attack_type(str), attack_category(str), power(int), enemy_defence(int), enemy_sp_defence(int), enemy_type(list)
        # check if the attack is effective (in multiple type of enemy)
        effectiveness = 1
        for ty in enemy_type:
            type_lower = ty.lower()
            effectiveness *= self.game.SETTINGS.type_chart[attack_type][type_lower]

        if attack_category == "physical":
            return math.floor(((((((2 * lvl / 5) + 2) * attack * power / enemy_defence) / 50 + 2) * effectiveness) * random.randint(217, 255)) / 255)  # physical attack
        elif attack_category == "special":
            return math.floor(((((((2 * lvl / 5) + 2) * attack_spe * power / enemy_sp_defence) / 50 + 2) * effectiveness) * random.randint(217, 255)) / 255)  # special attack
        else:
            return 0
            

    # TURN METHOD (manage the turn)
    def turn(self, move_choice=0):  # move_choice(1=attack, 2=switch, 3=bag | default(enemy_turn)=0)

        if move_choice == 0:
            self.attacker = self.__enemy_pokemon

        # ask the player what he want to do
        if self.attacker == self.__player_pokemon:
            if move_choice == 1:
                self.__last_move = self.__player_pokemon.get_moves()[int(self.__choice) - 1]["name"]
                self.__player_pokemon.get_current_move_pp()[int(self.__choice) - 1] -= 1
                damage = self.attack(self.__player_pokemon.get_lvl(), self.__player_pokemon.get_attack(), self.__player_pokemon.get_sp_attack(),
                                     self.__player_pokemon.get_moves()[int(self.__choice) - 1]["type"], self.__player_pokemon.get_moves()[int(self.__choice) - 1]["category"], self.__player_pokemon.get_moves()[int(self.__choice) - 1]["power"],
                                     self.__enemy_pokemon.get_defense(), self.__enemy_pokemon.get_sp_defense(), self.__enemy_pokemon.get_type())
                self.__enemy_pokemon.take_damage(damage)
                print(self.__player_pokemon.get_name() + " use " + self.__player_pokemon.get_moves()[int(self.__choice) - 1]["name"] + " and deal " + str(damage) + " damage")
                print(self.__enemy_pokemon.get_name() + " have " + str(self.__enemy_pokemon.get_hp()) + " hp left")

            elif move_choice == 2:
                self.switch_pokemon()

            # choice 3: bag | TODO: (ONLY FOR TEST IN TERMINAL - NOT FOR GUI VERSION DON'T FORGET TO REMOVE IT)
            elif move_choice == "3":
                print("Bag")

            # check if the enemy is dead (if yes, end the combat else next turn)
            if self.__enemy_pokemon.is_alive():
                if self.attacker == self.__player_pokemon:
                    self.attacker = self.__enemy_pokemon
                    self.__menu = 0
                    self.__choice = 1
                    self.__enemy_attack_next_turn = True
                else:
                    self.attacker = self.__player_pokemon
            else:
                self.win()

        # Make the enemy attack
        else:
            print("Enemy turn")
            # make the enemy choose a random attack
            choice = random.randint(0, len(self.__enemy_pokemon.get_moves()) - 1)
            self.__last_move = self.__enemy_pokemon.get_moves()[choice]["name"]
            # Make the enemy attack
            damage = self.attack(self.__enemy_pokemon.get_lvl(), self.__enemy_pokemon.get_attack(), self.__enemy_pokemon.get_sp_attack(),
                                 self.__enemy_pokemon.get_moves()[choice]["type"], self.__enemy_pokemon.get_moves()[choice]["category"], self.__enemy_pokemon.get_moves()[choice]["power"],
                                 self.__player_pokemon.get_defense(), self.__player_pokemon.get_sp_defense(), self.__player_pokemon.get_type())
            self.__player_pokemon.take_damage(damage)
            print(self.__enemy_pokemon.get_name() + " use " + self.__enemy_pokemon.get_moves()[choice]["name"] + " and deal " + str(damage) + " damage")
            print(self.__player_pokemon.get_name() + " have " + str(self.__player_pokemon.get_hp()) + " hp left")

            # check if the player is dead (if yes, end the combat else next turn)
            if self.__player_pokemon.is_alive():
                if self.attacker == self.__player_pokemon:
                    self.attacker = self.__enemy_pokemon
                else:
                    self.attacker = self.__player_pokemon
            else:
                self.lose()
                print("You lose !")

    # check who attack first (player or enemy) and return the pokemon who attack first (random if same speed)
    def check_who_attack_first(self):
        if self.__player_pokemon.get_speed() > self.__enemy_pokemon.get_speed():
            return self.__player_pokemon
        elif self.__player_pokemon.get_speed() < self.__enemy_pokemon.get_speed():
            return self.__enemy_pokemon
        else:
            return random.choice([self.__player_pokemon, self.__enemy_pokemon])

    # Make the player choose a pokemon to switch
    def switch_pokemon(self):
        print("Which pokemon do you want to switch ?")
        for i in range(0, len(self.game.Player.get_pokemons())):
            print(str(i + 1) + ". " + self.game.Player.get_pokemons()[i].get_name())
        choice = input("")

        # Check if the choice is valid
        if choice.isdigit() and 0 < int(choice) <= len(self.game.Player.get_pokemons()):
            self.__player_pokemon = self.game.Player.get_pokemons()[int(choice) - 1]
            print("You switch to " + self.__player_pokemon.get_name())
        else:
            print("Invalid choice")
            self.switch_pokemon()

    # make player go out of combat (cant run if the enemy is a trainer)
    def run(self):
        ood_escape = (((self.__player_pokemon.get_speed() * 128) / self.__enemy_pokemon.get_speed()) + 30 * self.__run_attempt) % 256
        if ood_escape > random.randint(0, 255):
            print("You run away")
            self.game.game_state = "map"
            del self
        else:
            print("You can't run away")
            self.__run_attempt += 1
            self.turn()  # if the player can't run, the enemy attack

    # function that calculate how much xp the player will get
    def calculate_xp(self):
        return math.floor(((self.__enemy_pokemon.get_lvl() * 2) + 10) / 250 * self.__enemy_pokemon.get_lvl()) + self.__enemy_pokemon.get_lvl() * 3

    # function that calculate how much money the player will get
    def calculate_money(self):
        return math.floor(self.__enemy_pokemon.get_lvl() * 1.5)

    # win the combat and give the player the reward
    def win(self):
        # give all players pokemon xp
        for pokemon in self.game.Player.get_pokemons():
            pokemon.add_xp(self.calculate_xp())
            pokemon.debug_all()

        # give the player money
        self.game.Player.add_money(self.calculate_money())

        print("You win !")
        print("You get " + str(self.calculate_xp()) + " xp and " + str(self.calculate_money()) + " money")
        self.game.game_state = "map"
        del self

    # lose the combat
    def lose(self):
        print("You lose !")
        self.game.game_state = "map"
        del self

    def input(self, event):
        if event.type == pygame.KEYDOWN and self.__intro_played and not self.__player_animation_hp and not self.__enemy_animation_hp and not self.__enemy_attack_next_turn:
            # Player choice #
            if event.key == pygame.K_ESCAPE:
                self.__menu = 0
                self.__choice = 1
            if event.key == pygame.K_RETURN:
                if self.__menu == 0:
                    if self.__choice == 1:
                        self.__menu = 1
                    if self.__choice == 2:
                        self.__menu = 2
                    if self.__choice == 3:
                        self.__menu = 3
                    if self.__choice == 4:
                        self.run()
                elif self.__menu == 1:
                    try:
                        self.turn(1)
                    except IndexError:
                        print("You can't use this move")

            if event.key == pygame.K_RIGHT:
                if self.__choice == 1 or self.__choice == 3:
                    self.__choice += 1
            if event.key == pygame.K_LEFT:
                if self.__choice == 2 or self.__choice == 4:
                    self.__choice -= 1
            if event.key == pygame.K_UP:
                if self.__choice == 3 or self.__choice == 4:
                    self.__choice -= 2
            if event.key == pygame.K_DOWN:
                if self.__choice == 1 or self.__choice == 2:
                    self.__choice += 2

    def draw(self, screen):

        # Update old hp bar (for animation) #
        if self.__enemy_pokemon_old_hp >= self.__enemy_pokemon.get_hp():
            self.__enemy_pokemon_old_hp -= 0.1
            self.__enemy_animation_hp = True
        else:
            self.__enemy_animation_hp = False
        if self.__player_pokemon_old_hp >= self.__player_pokemon.get_hp():
            self.__player_pokemon_old_hp -= 0.1
            self.__player_animation_hp = True
        else:
            self.__player_animation_hp = False
        # Check if the enemy attack next turn and if the animation is done #
        if not self.__enemy_animation_hp and self.__enemy_attack_next_turn:
            self.__enemy_attack_next_turn = False
            self.turn()


        # Background #
        screen.blit(self.game.SPRITES.forest_background, (0, 0))

        # Player Intro #
        screen.blit(self.game.SPRITES.get_combat_player_sprite(self.__player_sprite), (self.__player_sprite_x, 200))

        # PLAYER POKEMON #
        if self.__intro_played:
            self.play_summon_pokemon(screen)
            if self.__pokemon_spawned:
                scaled_pokemon_sprite = pygame.transform.scale(self.game.SPRITES.get_pokemon_sprite(self.__player_pokemon.get_id() + 1, "back"), (self.__pokemon_scale, self.__pokemon_scale))
                screen.blit(scaled_pokemon_sprite, (self.__pokemon__x, self.__pokemon__y))

        # Enemy Pokemon Status(HP_BAR, LVL, NAME)#
        screen.blit(self.game.SPRITES.enemy_pokemon_status, (80, 50))
        pygame.draw.rect(screen, self.hp_bar_color(self.__enemy_pokemon_old_hp, self.__enemy_pokemon), (275, 138, self.__enemy_pokemon_old_hp / self.__enemy_pokemon.get_max_hp() * 240, 15))
        self.game.SETTINGS.combat_font.render_to(screen, (490, 80), str(self.__enemy_pokemon.get_lvl()), size=60, fgcolor=self.game.COLORS.DARK_GRAY)
        self.game.SETTINGS.combat_font.render_to(screen, (120, 80), self.__enemy_pokemon.get_name(), size=60, fgcolor=self.game.COLORS.DARK_GRAY)

        # Player Pokemon Status(HP_BAR, LVL, NAME, HP, XP)#
        screen.blit(self.game.SPRITES.player_pokemon_status, (720, 345))
        pygame.draw.rect(screen, self.hp_bar_color(self.__player_pokemon_old_hp,self.__player_pokemon), (952, 413, self.__player_pokemon_old_hp / self.__player_pokemon.get_max_hp() * 230, 15))
        self.game.SETTINGS.combat_font.render_to(screen, (1160, 365), str(self.__player_pokemon.get_lvl()), size=60, fgcolor=self.game.COLORS.DARK_GRAY)
        self.game.SETTINGS.combat_font.render_to(screen, (800, 365), self.__player_pokemon.get_name(), size=60, fgcolor=self.game.COLORS.DARK_GRAY)
        self.game.SETTINGS.combat_font.render_to(screen, (1080, 435), str(round(self.__player_pokemon_old_hp)) + "/ " + str(self.__player_pokemon.get_max_hp()), size=55, fgcolor=self.game.COLORS.DARK_GRAY)
        # XP BAR #
        pygame.draw.rect(screen, self.game.COLORS.CYAN, (874, 479, self.__player_pokemon.get_exp() / (self.__player_pokemon.get_exp() + self.__player_pokemon.get_exp_to_next_level()) * 616, 8))

        # Bottom UI #
        screen.blit(self.game.SPRITES.bottom_message_box, (0, 500))
        if self.__menu == 0 and self.__intro_played and not self.__player_animation_hp and not self.__enemy_animation_hp and not self.__enemy_attack_next_turn:
            screen.blit(self.game.SPRITES.choice_box, (680, 500))
        elif self.__menu == 1:
            screen.blit(self.game.SPRITES.choice_move_box, (0, 500))

        # Pokemon #
        # Enemy Intro #
        self.play_summon_enemy_pokemon(screen)
        if not self.__enemy_pokemon_spawned:
            self.game.SETTINGS.combat_font.render_to(screen, (80, 550), "A wild " + self.__enemy_pokemon.get_name() + " appeared !", size=60, fgcolor=self.game.COLORS.WHITE)
        elif self.__enemy_pokemon_spawned and not self.__intro_played:
            self.game.SETTINGS.combat_font.render_to(screen, (80, 550), "GO " + self.__player_pokemon.get_name() + " !!!", size=60, fgcolor=self.game.COLORS.WHITE)

        # choice arrow
        if self.__menu == 0 and self.__intro_played and not self.__player_animation_hp and not self.__enemy_animation_hp and not self.__enemy_attack_next_turn:
            if self.__choice == 1:
                screen.blit(self.game.SPRITES.choice_arrow, (715, 555))
            elif self.__choice == 2:
                screen.blit(self.game.SPRITES.choice_arrow, (990, 555))
            elif self.__choice == 3:
                screen.blit(self.game.SPRITES.choice_arrow, (715, 625))
            elif self.__choice == 4:
                screen.blit(self.game.SPRITES.choice_arrow, (990, 625))
        elif self.__menu == 1:
            if self.__choice == 1:
                screen.blit(self.game.SPRITES.choice_arrow, (50, 555))
            elif self.__choice == 2:
                screen.blit(self.game.SPRITES.choice_arrow, (450, 555))
            elif self.__choice == 3:
                screen.blit(self.game.SPRITES.choice_arrow, (50, 625))
            elif self.__choice == 4:
                screen.blit(self.game.SPRITES.choice_arrow, (450, 625))

        # Text #
        if self.__menu == 0 and self.__intro_played and not self.__enemy_animation_hp and not self.__player_animation_hp:
            self.game.SETTINGS.combat_font.render_to(screen, (80, 550), "What will " + self.__player_pokemon.get_name() + " do ?", size=60, fgcolor=self.game.COLORS.WHITE)
        elif self.__menu == 1:
            x = 100
            y = 550
            # player pokemon moves
            for i in range(4):
                try:
                    self.game.SETTINGS.combat_font.render_to(screen, (x, y), self.__player_pokemon.get_moves()[i]["name"].upper(), size=100, fgcolor=self.game.COLORS.DARK_GRAY)
                except IndexError:
                    y += 25
                    self.game.SETTINGS.combat_font.render_to(screen, (x, y), "--", size=100, fgcolor=self.game.COLORS.DARK_GRAY)
                    y -= 25
                x += 400
                if i == 1:
                    x = 100
                    y = 620
            # player current selected move pp and max pp and type
            try:
                self.game.SETTINGS.combat_font.render_to(screen, (1080, 550), str(self.__player_pokemon.get_current_move_pp()[self.__choice - 1]), size=80, fgcolor=self.game.COLORS.DARK_GRAY)
                self.game.SETTINGS.combat_font.render_to(screen, (1180, 550), str(self.__player_pokemon.get_moves()[self.__choice - 1]["pp"]), size=80, fgcolor=self.game.COLORS.DARK_GRAY)
                self.game.SETTINGS.combat_font.render_to(screen, (1040, 635), self.__player_pokemon.get_moves()[self.__choice - 1]["type"].upper(), size=70, fgcolor=self.game.COLORS.DARK_GRAY)
            except IndexError:
                pass

        # pokemon as use a move #
        if self.__enemy_animation_hp:
            self.game.SETTINGS.combat_font.render_to(screen, (80, 550), self.__player_pokemon.get_name() + " as used " + self.__last_move, size=60, fgcolor=self.game.COLORS.WHITE)
        elif self.__player_animation_hp:
            self.game.SETTINGS.combat_font.render_to(screen, (80, 550), self.__enemy_pokemon.get_name() + " as used " + self.__last_move, size=60, fgcolor=self.game.COLORS.WHITE)

        # Player Intro
        if self.__enemy_pokemon_x <= 800:
            if not self.__intro_played:
                if self.__player_sprite_x < 0:
                    self.__player_sprite_x += 10
                else:
                    self.play_player_intro()
            else:
                if self.__player_sprite_x > -400:
                    self.__player_sprite_x -= 10

    def play_player_intro(self):
        if self.game.current_time - self.game.last_time >= self.game.SPRITES.player_intro_speed:
            self.__player_sprite += 1
            self.game.last_time = self.game.current_time
            if self.__player_sprite == 5:
                self.__intro_played = True
                self.__player_sprite = 1

    def play_summon_pokemon(self, screen):
        player_pokemon_sprite = self.game.SPRITES.get_pokemon_sprite(self.__player_pokemon.get_id() + 1, "back")
        player_pokemon_sprite.fill((255, self.__spawn_color, 255), special_flags=pygame.BLEND_RGB_MAX)
        scaled_pokemon_sprite = pygame.transform.scale(player_pokemon_sprite, (self.__pokemon_scale, self.__pokemon_scale))
        if self.__pokemon_scale < 300:
            self.__pokemon_scale += 10
            self.__spawn_color -= 5
            self.__pokemon__y -= 5
            self.__pokemon__x -= 5
            screen.blit(scaled_pokemon_sprite, (self.__pokemon__x, self.__pokemon__y))
        else:
            self.__pokemon_spawned = True

    def play_summon_enemy_pokemon(self, screen):
        if self.__enemy_pokemon_x > 800:
            self.__enemy_pokemon_x -= 10
        else:
            self.__enemy_pokemon_spawned = True
        screen.blit(self.game.SPRITES.get_pokemon_sprite(self.__enemy_pokemon.get_id() + 1, "front"), (self.__enemy_pokemon_x, 70))

    def hp_bar_color(self, pokemon_hp, pokemon):
        if pokemon_hp <= pokemon.get_max_hp() * 0.25:
            return self.game.COLORS.RED
        elif pokemon_hp <= pokemon.get_max_hp() * 0.5:
            return self.game.COLORS.YELLOW
        else:
            return self.game.COLORS.GREEN
