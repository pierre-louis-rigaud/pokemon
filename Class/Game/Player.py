class Player:
    def __init__(self):
        self.__name = "ABCDEF"  # Name of the player (max 6 char)
        self.__pokemons = []  # List of the pokemons of the player
        self.__money = 0  # Money of the player
        self.__badges = []  # List of the badges of the player
        self.__items = []  # List of the items of the player

    # Getters #

    # get the name of the player #
    def get_name(self):
        return self.__name

    # get the pokemons of the player #
    def get_pokemons(self):
        return self.__pokemons

    # get the money of the player #
    def get_money(self):
        return self.__money

    # get the badges of the player #
    def get_badges(self):
        return self.__badges

    # get the items of the player #
    def get_items(self):
        return self.__items

    # POKEMON SETTERS #

    # Add pokemon to the player #
    def add_pokemons(self, pokemon):
        if len(self.__pokemons) < 6:
            self.__pokemons.append(pokemon)

    # Remove pokemon from the player #
    def remove_pokemons(self, pokemon):
        self.__pokemons.remove(pokemon)

    # Add money to the player #
    def add_money(self, money):
        self.__money += money
