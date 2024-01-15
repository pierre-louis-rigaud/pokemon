import math


class Pokemon:
    def __init__(self, game, pokemon_id, iv, ev, nature, level, moves, shiny):  # IV = Individual Value, EV = Effort Value, nature = Nature, level = Level, moves = Moves, shiny = Shiny

        # GAME #
        self.__GAME = game

        # BASE STATS (depending on level) #
        # THEY ARE NOT USED IN COMBAT #

        self.__ID = pokemon_id - 1  # id of the pokemon (ex: 25 [for Pikachu])
        self.__NAME = self.__GAME.SETTINGS.pokedex[self.__ID]["name"][self.__GAME.SETTINGS.language]  # name of the pokemon  (ex: "Pikachu")
        self.__TYPE = self.__GAME.SETTINGS.pokedex[self.__ID]["type"]  # type of the pokemon (ex: ["Fire", "Flying"])
        self.__MAX_HP = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["HP"]  # max hp of the pokemon (ex: 35)
        self.__ATTACK = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Attack"]  # attack of the pokemon (ex: 55)
        self.__DEFENSE = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Defense"]  # defense of the pokemon (ex: 40)
        self.__SP_ATTACK = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Sp. Attack"]  # sp. attack of the pokemon (ex: 50)
        self.__SP_DEFENCE = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Sp. Defense"]  # sp. defense of the pokemon  (ex: 50)
        self.__SPEED = self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Speed"]  # speed of the pokemon  (ex: 90)

        # MOVE SET #
        self.__moves = self.initialize_moves(moves)  # moves of the pokemon (ex: ["Tackle", "Growl", "Thunder Shock", "Quick Attack"])
        self.__current_move_PP = [move["pp"] for move in self.__moves]  # current pp of the moves of the pokemon (ex: [35, 40, 30, 40])

        # LEVEL UP STATS #

        self.__LEVEL = level  # level of the pokemon
        self.__EXP = 0  # current exp of the pokemon
        self.__EXP_TO_NEXT_LEVEL = 0  # exp to next level of the pokemon

        # COMBAT STATS #
        # ONLY THIS STATS ARE USED IN COMBAT #

        self.STATUS = "None"  # status of the pokemon (poison, burn, sleep, etc.)
        self.CURRENT_HP = self.__MAX_HP  # current hp of the pokemon
        self.CURRENT_ATTACK = self.__ATTACK  # current attack of the pokemon
        self.CURRENT_DEFENSE = self.__DEFENSE  # current defense of the pokemon
        self.CURRENT_SP_ATTACK = self.__SP_ATTACK  # current sp attack of the pokemon
        self.CURRENT_SP_DEFENSE = self.__SP_DEFENCE  # current sp defense of the pokemon
        self.CURRENT_SPEED = self.__SPEED  # current speed of the pokemon
        self.CURRENT_ACCURACY = 1  # current accuracy of the pokemon
        self.CURRENT_EVASION = 1  # current evasion of the pokemon

        # ___________________________________ #

        # STATS RANDOMLY GENERATED #

        self.__IV = iv  # individual value of the pokemon
        self.__EV = ev  # effort value of the pokemon
        self.__NATURE = nature  # nature of the pokemon
        self.__SHINY = shiny  # shiny of the pokemon

        # CALCULATE STATS #

        self.calculate_stat()  # calculate all stats of the pokemon
        self.calculate_exp_to_next_level()  # calculate the exp to next level of the pokemon
        self.debug_all()  # debug all stats of the pokemon

    # _____GETTERS_____ #

    # get the id of the pokemon #
    def get_id(self):
        return self.__ID

    # get the current moves of the pokemon #
    def get_moves(self):
        return self.__moves

    # get the current move pp of the pokemon #
    def get_current_move_pp(self):
        return self.__current_move_PP

    # get defense of the pokemon #
    def get_defense(self):
        return self.CURRENT_DEFENSE

    # get sp defense of the pokemon #
    def get_sp_defense(self):
        return self.CURRENT_SP_DEFENSE

    # get the current attack of the pokemon #
    def get_attack(self):
        return self.CURRENT_ATTACK

    # get the current sp attack of the pokemon #
    def get_sp_attack(self):
        return self.CURRENT_SP_ATTACK

    # get the current speed of the pokemon #
    def get_speed(self):
        return self.CURRENT_SPEED

    # get the current hp of the pokemon #
    def get_hp(self):
        return self.CURRENT_HP

    # get the max hp of the pokemon #
    def get_max_hp(self):
        return self.__MAX_HP

    # get the type of the pokemon #
    def get_type(self):
        return self.__TYPE

    # get the name of the pokemon #
    def get_name(self):
        return self.__NAME

    # get the lvl of the pokemon #
    def get_lvl(self):
        return self.__LEVEL

    # get if the pokemon is shiny #
    def get_shiny(self):
        return self.__SHINY

    # get the exp of the pokemon #
    def get_exp(self):
        return self.__EXP

    # get the exp to next level of the pokemon #
    def get_exp_to_next_level(self):
        return self.__EXP_TO_NEXT_LEVEL

    # _____SETTERS_____ #

    # set the current attack of the pokemon
    def set_attack(self, attack):
        self.__ATTACK = attack

    # set the current sp attack of the pokemon
    def set_sp_attack(self, sp_attack):
        self.__SP_ATTACK = sp_attack

    # set the current defense of the pokemon
    def set_defense(self, defense):
        self.__DEFENSE = defense

    # set the current sp defense of the pokemon
    def set_sp_defense(self, sp_defense):
        self.__SP_DEFENCE = sp_defense

    # set the current speed of the pokemon
    def set_speed(self, speed):
        self.__SPEED = speed

    # set the current hp of the pokemon
    def set_hp(self, hp):
        self.__MAX_HP = hp

    # set the current xp of the pokemon
    def set_exp(self, exp):
        self.__EXP = exp
    # ____________________STATS_____________________ #

    # calculate the stats of the pokemon
    def calculate_stat(self):

        # HP #
        self.__MAX_HP = math.floor((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["HP"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + self.__LEVEL + 10

        # ATTACK #
        self.__ATTACK = math.floor(((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Attack"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + 5) + self.__GAME.SETTINGS.natures[self.__NATURE]["Attack"]

        # DEFENSE #
        self.__DEFENSE = math.floor(((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Defense"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + 5) + self.__GAME.SETTINGS.natures[self.__NATURE]["Defense"]

        # SP.ATTACK #
        self.__SP_ATTACK = math.floor(((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Sp. Attack"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + 5) + self.__GAME.SETTINGS.natures[self.__NATURE]["AttackSPE"]

        # SP.DEFENSE #
        self.__SP_DEFENCE = math.floor(((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Sp. Defense"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + 5) + self.__GAME.SETTINGS.natures[self.__NATURE]["DefenseSPE"]
        # SPEED #
        self.__SPEED = math.floor(((2 * self.__GAME.SETTINGS.pokedex[self.__ID]["base"]["Speed"] + self.__IV + math.floor(self.__EV / 4)) * self.__LEVEL / 100) + 5) + self.__GAME.SETTINGS.natures[self.__NATURE]["Speed"]

        # set the current stats of the pokemon
        self.set_current_stats()

    # set the current stats of the pokemon (to use at the end of a battle)
    def set_current_stats(self):
        self.CURRENT_HP = self.__MAX_HP  # set the current hp to the max hp
        self.CURRENT_ATTACK = self.__ATTACK  # set the current attack to the attack
        self.CURRENT_DEFENSE = self.__DEFENSE  # set the current defense to the defense
        self.CURRENT_SP_ATTACK = self.__SP_ATTACK  # set the current sp attack to the sp attack
        self.CURRENT_SP_DEFENSE = self.__SP_DEFENCE  # set the current sp defense to the sp defense
        self.CURRENT_SPEED = self.__SPEED  # set the current speed to the speed

    # calculate the exp to the next level
    def calculate_exp_to_next_level(self):
        self.__EXP_TO_NEXT_LEVEL = math.floor(4 * (self.__LEVEL ** 3) / 5)

    # initialize the moves of the pokemon
    def initialize_moves(self, moves):
        m = []
        for move in moves:
            m.append(self.__GAME.SETTINGS.moves[move])
        return m

    # add xp to the pokemon (if the pokemon has enough xp to level up, it will level up)
    def add_xp(self, xp):
        self.__EXP += xp
        if self.__EXP >= self.__EXP_TO_NEXT_LEVEL:
            self.level_up()

    # _________________CHANGE_STATUS________________ #

    # level up the pokemon (increase the level by 1 and recalculate the stats)
    def level_up(self):
        self.__LEVEL += 1
        self.__EXP = 0
        self.calculate_stat()
        self.calculate_exp_to_next_level()
        print(f"{self.__NAME} has leveled up ! It's now level {self.__LEVEL} !")

    # heal the pokemon (heal to max hp if it's alive)
    def heal(self, hp):
        if self.is_alive():
            self.CURRENT_HP += hp
            if self.CURRENT_HP > self.__MAX_HP:
                self.CURRENT_HP = self.__MAX_HP
        else:
            print("The pokemon is dead, you can't heal it !")

    # cure the pokemon (heal to max hp even if it's dead and reload the PP Used in POKE_CENTER)
    def cure(self):
        self.reload_moves()
        self.CURRENT_HP = self.__MAX_HP
        self.STATUS = "None"
        print("The pokemon is cured !")

    # reload the moves of the pokemon (reload the PP Used in POKE_CENTER)
    def reload_moves(self):
        self.__current_move_PP = [self.__moves[0]["pp"], self.__moves[1]["pp"], self.__moves[2]["pp"], self.__moves[3]["pp"]]
        print("The pokemon's PP have been reloaded !")

    # change the status of the pokemon (poison, burn, sleep, etc.)
    def change_status(self, status):
        self.STATUS = status
        print(f"{self.__NAME} is now {status} !")

    # ____________________COMBAT____________________ #

    # check if the pokemon is alive
    def is_alive(self):
        return self.CURRENT_HP > 0

    # take damage to the pokemon (if the pokemon is dead, it will set the hp to 0)
    def take_damage(self, damage):
        self.CURRENT_HP -= damage
        if self.CURRENT_HP < 0:
            self.CURRENT_HP = 0

    # use a move (if the pokemon has enough PP, it will use the move)
    def use_pp(self, move):
        if self.__current_move_PP[move] > 0:
            self.__current_move_PP[move] -= 1
        else:
            print("Not enough PP !")

    # ____________________DEBUG_____________________ #

    # print the stats of the pokemon
    def debug_stat(self):
        print(f"_____________________DEBUG_STATS()____________________\n"
              f"NAME: {self.__NAME}\n"
              f"HP: {self.__MAX_HP}\n"
              f"TYPE: {self.__TYPE}\n"
              f"ATTACK: {self.__ATTACK}\n"
              f"DEFENSE: {self.__DEFENSE}\n"
              f"SP.ATTACK: {self.__SP_ATTACK}\n"
              f"SP.DEFENCE: {self.__SP_DEFENCE}\n"
              f"SPEED: {self.__SPEED}\n"
              f"IV: {self.__IV}\n"
              f"EV: {self.__EV}\n"
              f"NATURE: {self.__NATURE}\n"
              f"SHINY: {self.__SHINY}\n")

    def debug_current_stat(self):
        print(f"_____________________DEBUG_CURRENT_STATS()____________________\n"
              f"HP: {self.CURRENT_HP}\n"
              f"ATTACK: {self.CURRENT_ATTACK}\n"
              f"DEFENSE: {self.CURRENT_DEFENSE}\n"
              f"SP.ATTACK: {self.CURRENT_SP_ATTACK}\n"
              f"SP.DEFENCE: {self.CURRENT_SP_DEFENSE}\n"
              f"SPEED: {self.CURRENT_SPEED}\n"
              f"______________________________________________________________\n")

    def debug_moves(self):
        print(f"_____________________DEBUG_MOVES()____________________\n"
              f"MOVES_NAME: {[move['name'] for move in self.__moves]}\n"
              f"MOVES_POWER: {[move['power'] for move in self.__moves]}\n"
              f"MOVES_ACCURACY: {[move['accuracy'] for move in self.__moves]}\n"
              f"MOVES_TYPE: {[move['type'] for move in self.__moves]}\n"
              f"MOVES_CATEGORY: {[move['category'] for move in self.__moves]}\n"
              f"MOVES_PP: {[move['pp'] for move in self.__moves]}\n"
              f"CURRENT_MOVES_PP: {self.__current_move_PP}\n"
              f"MOVES_ACCURACY: {[move['accuracy'] for move in self.__moves]}\n"
              f"______________________________________________________\n")

    def debug_status(self):
        print(f"_____________________DEBUG_STATUS()____________________\n"
              f"STATUS: {self.STATUS}\n"
              f"________________________________________________________\n")

    def debug_level(self):
        print(f"_____________________DEBUG_LEVEL()____________________\n"
              f"LEVEL: {self.__LEVEL}\n"
              f"EXP: {self.__EXP}\n"
              f"EXP_TO_NEXT_LEVEL: {self.__EXP_TO_NEXT_LEVEL}\n"
              f"______________________________________________________\n")

    def debug_all(self):
        self.debug_stat()
        self.debug_moves()
        self.debug_current_stat()
        self.debug_status()
        self.debug_level()
