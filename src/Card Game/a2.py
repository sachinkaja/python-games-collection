from a2_support import *

class Card():
    """
    An abstract class from which all instantiable types of cards inheret.
    Provides the default card behaviour, which can be inhereted or
    overwritten by specific types of cards.
    """

    def get_damage_amount(self) -> int:
        """
        Returns the amount of damage this card does to its target.

        Parameters:
        self: The card object to check the damage amount.

        Returns:
        Damage amount as an integer. By default it returns 0.
        """
        
        return 0

    def get_block(self) -> int:
        """
        Returns the amount of block this card adds to its user.

        Parameters:
        self: The card object to check the block.

        Returns:
        Block value as an integer. By default it returns 0.
        """
        
        return 0

    def get_energy_cost(self) -> int:
        """
        Returns the amount of energy this card costs to play.

        Parameters:
        self: The card object to check the energy cost.

        Returns:
        Energy cost as an integer. By default it returns 1.
        """
        
        return 1

    def get_status_modifiers(self) -> dict[str, int]:
        """
        Returns a dictionary describing each status modifiers applied
        when this card is played.

        Parameters:
        self: The card object to check the status modifiers.

        Returns:
        Status modifiers as a dictionary. By default it returns
        empty dictionary.
        """
        
        result = {}
        return result

    def get_name(self) -> str:
        """
        Returns the name of the card.

        Parameters:
        self: The card object to check the name.

        Returns:
        Name of the card as a string. By default it returns 'Card'.
        """
        
        return type(self).__name__

    def get_description(self) -> str:
        """
        Returns a description of the card.

        Parameters:
        self: The card object to check the description.

        Returns:
        Description of the card as a string. By default it returns 'A card'.
        """
        
        return "A card."

    def requires_target(self) -> bool:
        """
        Returns True if playing this card requires a target,
        and False if it does not.

        Parameters:
        self: The card object to check the requires target.

        Returns:
        Target required of the card as a boolean. By default it returns True.
        """
        
        return True

    def __str__(self) -> str:
        """
        Returns the string representation for the card,
        in the format ‘{Card name}: {Card description}’.

        Parameters:
        self: The card object to check the string representation.

        Returns:
        Card representation as a string.
        """
        
        return f"{self.get_name()}: {self.get_description()}"

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new
        instance of this class identical to self.

        Parameters:
        self: The card object to check the text for creating a new instance.

        Returns:
        New instance text as a string.
        """
        
        return f"{self.get_name()}()"

class Strike(Card):
    """
    Strike is a type of Card that deals 6 damage to its target.
    It costs 1 energy point to play.
    """

    def get_damage_amount(self) -> int:
        return 6

    def get_description(self) -> str:
        return "Deal 6 damage."

class Defend(Card):
    """
    Defend is a type of Card that adds 5 block to its user.
    Defend does not require a target. It costs 1 energy point to play.
    """

    def get_block(self) -> int:
        return 5

    def get_description(self) -> str:
        return "Gain 5 block."

    def requires_target(self) -> bool:
        return False

class Bash(Card):
    """
    Bash is a type of Card that adds 5 block to its user and causes 7 damage
    to its target. It costs 2 energy points to play.
    """

    def get_damage_amount(self) -> int:
        return 7

    def get_block(self) -> int:
        return 5

    def get_energy_cost(self) -> int:
        return 2

    def get_description(self) -> str:
        return "Deal 7 damage. Gain 5 block."

class Neutralize(Card):
    """
    Neutralize is a type of card that deals 3 damage to its target.
    It also applies status modifiers to its target; namely,
    it applies 1 weak and 2 vulnerable. Neutralize does not cost any energy
    points to play.
    """

    def get_damage_amount(self) -> int:
        return 3

    def get_energy_cost(self) -> int:
        return 0

    def get_status_modifiers(self) -> dict[str, int]:
        result = {"weak": 1, "vulnerable": 2}
        return result

    def get_description(self) -> str:
        return "Deal 3 damage. Apply 1 weak. Apply 2 vulnerable."

class Survivor(Card):
    """
    Survivor is a type of card that adds 8 block and applies 1 strength to
    its user. Survivor does not require a target.
    """
    
    def get_block(self) -> int:
        return 8

    def get_status_modifiers(self) -> dict[str, int]:
        result = {"strength": 1}
        return result

    def get_description(self) -> str:
        return "Gain 8 block and 1 strength."

    def requires_target(self) -> bool:
        return False

class Eruption(Card):
    """
    Eruption is a type of card which costs 2 energy points to play,
    and deals 9 damage to its target.
    """

    def get_damage_amount(self) -> int:
        return 9

    def get_energy_cost(self) -> int:
        return 2

    def get_description(self) -> str:
        return "Deal 9 damage."

class Vigilance(Card):
    """
    Vigilance is a type of card which costs 2 energy points to play and adds 8
    block and 1 strength to its user. It does not require a target.
    """

    def get_block(self) -> int:        
        return 8

    def get_energy_cost(self) -> int:
        return 2

    def get_status_modifiers(self) -> dict[str, int]:
        result = {"strength": 1}
        return result

    def get_description(self) -> str:
        return "Gain 8 block and 1 strength."

    def requires_target(self) -> bool:
        return False

class Entity():
    """
    Abstract base class from which all entities inherit.
    Provides the default entity behaviour, which can be inhereted or
    overwritten by player or monster.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Sets up a new entity with the given max_hp. An entity starts with
        the maximum amount of HP it can have. Block, strength, weak,
        and vulnerable all start at 0.

        Parameters:
        self: The entity object to initialize.
        max_hp: The maximum HP the entity object can have.

        Returns:
        None
        """
        
        self._hp = self._max_hp = max_hp
        self._block = self._strength = self._weak = self._vulnerable = 0

    def get_hp(self) -> int:
        """
        Returns the current HP for this entity.

        Parameters:
        self: The entity object to get the HP.

        Returns:
        HP value as an integer.
        """

        return self._hp

    def get_max_hp(self) -> int:
        """
        Returns the maximum possible HP for this entity.

        Parameters:
        self: The entity object to get the maximum HP.

        Returns:
        Maximum HP value as an integer.
        """

        return self._max_hp

    def get_block(self) -> int:
        """
        Returns the amount of block for this entity.

        Parameters:
        self: The entity object to get the block.

        Returns:
        Block value as an integer.
        """

        return self._block

    def get_strength(self) -> int:
        """
        Returns the amount of strength for this entity.

        Parameters:
        self: The entity object to get the strength.

        Returns:
        Strength value as an integer.
        """

        return self._strength

    def get_weak(self) -> int:
        """
        Returns the number of turns for which this entity is weak.

        Parameters:
        self: The entity object to get the number of turns the entity is weak.

        Returns:
        Number of turns as an integer.
        """

        return self._weak

    def get_vulnerable(self) -> int:
        """
        Returns the number of turns for which this entity is vulnerable.

        Parameters:
        self: The entity object to get the number of turns the
        entity is vulnerable.

        Returns:
        Number of turns as an integer.
        """

        return self._vulnerable

    def get_name(self) -> str:
        """
        Returns the name of the entity. The name of an entity is just
        the name of the most specific class it belongs to.

        Parameters:
        self: The entity object to get the name.

        Returns:
        Name of the entity object as a string.
        """

        return type(self).__name__

    def reduce_hp(self, amount: int) -> None:
        """
        Attacks the entity with a damage of amount. This involves reducing
        block until the amount of damage has been done or until
        block has reduced to zero, in which case the HP is reduced by the
        remaining amount.

        Parameters:
        self: The entity object for which the hp needs to be reduced.
        amount: The damage amount.

        Returns:
        None.
        """

        if amount <= self._block:
            self._block -= amount
        elif self._block < amount <= self._hp:
            amount -= self._block
            self._hp -= amount
            self._block = 0
        elif self._hp < amount:
            self._block = 0
            self._hp = 0

    def is_defeated(self) -> bool:
        """
        Returns True if the entity is defeated, and False otherwise.
        An entity is defeated if it has no HP remaining.

        Parameters:
        self: The entity object for which defeated is checked.

        Returns:
        Is defeated as a boolean.
        """

        return self._hp == 0

    def add_block(self, amount: int) -> None:
        """
        Adds the given amount to the amount of block this entity has.

        Parameters:
        self: The entity object for which block needs to be added.
        amount: The additional block amount.

        Returns:
        None.
        """

        self._block += amount

    def add_strength(self, amount: int) -> None:
        """
        Adds the given amount to the amount of strength this entity has.

        Parameters:
        self: The entity object for which strength needs to be added.
        amount: The additional strength amount.

        Returns:
        None.
        """

        self._strength += amount

    def add_weak(self, amount: int) -> None:
        """
        Adds the given amount to the amount of weak this entity has.

        Parameters:
        self: The entity object for which weak needs to be added.
        amount: The additional weak amount.

        Returns:
        None.
        """

        self._weak += amount

    def add_vulnerable(self, amount: int) -> None:
        """
        Adds the given amount to the amount of vulnerable this entity has.

        Parameters:
        self: The entity object for which vulnerable needs to be added.
        amount: The additional vulnerable amount.

        Returns:
        None.
        """

        self._vulnerable += amount

    def new_turn(self) -> None:
        """
        Applies any status changes that occur when a new turn begins.
        For the base Entity class, this involves setting block back to 0,
        and reducing weak and vulnerable each by 1 if they are greater than 0.

        Parameters:
        self: The entity object.

        Returns:
        None.
        """

        self._block = 0
        
        if self._weak > 0:
            self._weak -= 1
            
        if self._vulnerable > 0:
            self._vulnerable -= 1

    def __str__(self) -> str:
        """
        Returns the string representation for the entity in the format
        ‘{entity name}: {current HP}/{max HP} HP’.

        Parameters:
        self: The entity object to check the string representation.

        Returns:
        Entity representation as a string.
        """
        
        return f"{self.get_name()}: {self._hp}/{self._max_hp} HP"

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance
        of this class identical to self.

        Parameters:
        self: The entity object to check the text for creating a new instance.

        Returns:
        New instance text as a string.
        """
        
        return f"{self.get_name()}({self._max_hp})"

class Player(Entity):
    """
    A Player is a type of entity that the user controls. In addition to
    regular entity functionality, a player also has energy and cards.
    Player’s must manage three sets of cards; the deck(cards remaining
    to be drawn), their hand(cards playable in the current turn), and a
    discard pile(cards that have been played already this encounter).
    """

    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        """
        Initializes the player object with the deck of cards and
        energy to 3 along with regular initialization of entity class.

        Parameters:
        self: The player object.
        max_hp: The maximum HP the player object can have.
        cards: The deck of cards for the player.

        Returns:
        None.
        """
        
        super().__init__(max_hp)
        self._energy = 3

        self._deck = []
        if cards != None and len(cards) > 0:
            self._deck = cards

        self._hand = []
        self._discarded = []

    def get_energy(self) -> int:
        """
        Returns the amount of energy the player has remaining.

        Parameters:
        self: The player object.

        Returns:
        The energy of the player as integer.
        """

        return self._energy

    def get_hand(self) -> list[Card]:
        """
        Returns the players current hand.

        Parameters:
        self: The player object.

        Returns:
        Players cards in hand as a list.
        """

        return self._hand

    def get_deck(self) -> list[Card]:
        """
        Returns the players current deck.

        Parameters:
        self: The player object.

        Returns:
        Players cards in deck as a list.
        """

        return self._deck

    def get_discarded(self) -> list[Card]:
        """
        Returns the players current discarded pile.

        Parameters:
        self: The player object.

        Returns:
        Players cards in discarded pile as a list.
        """

        return self._discarded

    def start_new_encounter(self) -> None:
        """
        Adds all cards from the player’s discard pile to the end of their
        deck, and sets the discard pile to be an empty list.

        Parameters:
        self: The player object.

        Returns:
        None.
        """

        self._deck += self._discarded
        self._discarded = []

    def end_turn(self) -> None:
        """
        Adds all remaining cards from the player’s hand to the end of their
        discard pile, and sets their hand back to an empty list.

        Parameters:
        self: The player object.

        Returns:
        None.
        """

        self._discarded += self._hand
        self._hand = []

    def new_turn(self) -> None:
        """
        This method sets the player up for a new turn. This involves
        everything that a regular entity requires for a new turn, but
        also requires that the player be dealt a new hand of 5 cards,
        and energy be reset to 3.

        Parameters:
        self: The player object.

        Returns:
        None.
        """

        super().new_turn()
        draw_cards(self._deck, self._hand, self._discarded)
        self._energy = 3

    def play_card(self, card_name: str) -> Card | None:
        """
        Attempts to play a card from the player’s hand if card is availble
        and player has enough energy.

        Parameters:
        self: The player object.
        card_name: Name of the card, the player wants to play.

        Returns:
        If card is played, then returns the card else it returns None.
        """

        for card in self._hand:
            if card_name == card.get_name():
                energy_required = card.get_energy_cost()
                if energy_required <= self._energy:
                    self._discarded.append(card)
                    self._hand.remove(card)
                    self._energy -= energy_required
                    return card

    def __repr__(self) -> str:
        if self._deck == None or len(self._deck) <= 0:
            return super().__repr__()

        cards = [Strike(), Defend(), Bash(), Neutralize(), Survivor()]
        return f"{self.get_name()}({self.get_max_hp()}, {cards})"

class IronClad(Player):
    """
    IronClad is a type of player that starts with 80 HP. IronClad’s deck
    contains 5 Strike cards, 4 Defend cards, and 1 Bash card.
    """

    def __init__(self) -> None:
        """
        Initializes the IronClad player object with 5 Strike cards,
        4 Defend cards, and 1 Bash card. The max HP is 80.

        Parameters:
        self: The IronClad object.

        Returns:
        None.
        """
        
        cards = generate_player_cards(self.get_name())
        super().__init__(80, cards)

    def __repr__(self) -> str:
        return f"{self.get_name()}()"

class Silent(Player):
    """
    Silent is a type of player that starts with 70 HP. Silent’s deck
    contains 5 Strike cards, 5 Defend cards, 1 Neutralize card, and
    1 Survivor card.
    """

    def __init__(self) -> None:
        """
        Initializes the Silent player object with 5 Strike cards,
        5 Defend cards, 1 Neutralize card, and 1 Survivor card.
        The max HP is 70.

        Parameters:
        self: The Silent object.

        Returns:
        None.
        """
        
        cards = generate_player_cards(self.get_name())
        super().__init__(70, cards)

    def __repr__(self) -> str:
        return f"{self.get_name()}()"

class Watcher(Player):
    """
    Watcher is a type of player that starts with 72 HP. Watcher’s deck
    contains 4 Strike cards, 4 Defend cards, 1 Eruption card, and
    1 Vigilance card.
    """

    def __init__(self) -> None:
        """
        Initializes the Watcher player object with 4 Strike cards,
        4 Defend cards, 1 Eruption card, and 1 Vigilance card.
        The max HP is 70.

        Parameters:
        self: The Watcher object.

        Returns:
        None.
        """
        
        cards = generate_player_cards(self.get_name())
        super().__init__(72, cards)

    def __repr__(self) -> str:
        return f"{self.get_name()}()"

class Monster(Entity):
    """
    A Monster is a type of entity that the user battles during encounters.
    In addition to regular entity functionality, each monster also has a
    unique id, and an action method that handles the effects of the
    monster’s action on itself, and describes the effect the monster’s
    action would have on its target.
    """

    unique_id = 0

    def __init__(self, max_hp: int) -> None:
        """
        Initializes the monster object with regular entity class.

        Parameters:
        self: The monster object.
        max_hp: The maximum HP the monster object can have.

        Returns:
        None.
        """
        
        super().__init__(max_hp)

        self._monster_id = Monster.unique_id
        Monster.unique_id += 1

    def get_id(self) -> int:
        """
        Returns the unique id number of this monster.

        Parameters:
        self: The monster object.

        Returns:
        Unique id as an integer.
        """

        return self._monster_id

    def action(self) -> dict[str, int]:
        """
        Performs the current action for this monster, and returns a
        dictionary describing the effects this monster’s action should
        cause to its target.

        Parameters:
        self: The monster object.

        Returns:
        Action of the monster as a dictionary.
        """
        
        raise NotImplementedError

class Louse(Monster):
    """
    Louse is a monster object which has only one action defined - damage.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes the louse object with regular monster class.

        Parameters:
        self: The louse object.
        max_hp: The maximum HP the louse object can have.

        Returns:
        None.
        """
        
        super().__init__(max_hp)
        self._amount = random_louse_amount()

    def action(self) -> dict[str, int]:
        """
        The Louse’s action method simply returns a dictionary of
        {‘damage’:amount}, where amount is between 5 and 7 (inclusive).

        Parameters:
        self: The louse object.

        Returns:
        Action of the louse monster as a dictionary.
        """

        actions = {"damage": self._amount}
        return actions

class Cultist(Monster):
    """
    Cultist is a monster object which has two actions defined - damage
    and weak.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes the cultist object with regular monster class.

        Parameters:
        self: The cultist object.
        max_hp: The maximum HP the cultist object can have.

        Returns:
        None.
        """
        
        super().__init__(max_hp)
        self._damage_amount = 0
        self._weak_amount = False

    def action(self) -> dict[str, int]:
        """
        The action method for Cultist should return a dictionary of
        {‘damage’: damage_amount, ‘weak’: weak_amount}.

        Parameters:
        self: The cultist object.

        Returns:
        Action of the cultist monster as a dictionary.
        """

        actions = {"damage": self._damage_amount,\
                   "weak": int(self._weak_amount)}

        if self._damage_amount == 0:
            self._damage_amount = 6
        self._damage_amount += 1
        self._weak_amount = not self._weak_amount

        return actions

class JawWorm(Monster):
    """
    JawWorm is a monster object which has only one action - damage.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes the JawWorm object with regular monster class.

        Parameters:
        self: The JawWorm object.
        max_hp: The maximum HP the JawWorm object can have.

        Returns:
        None.
        """
        
        super().__init__(max_hp)

    def action(self) -> dict[str, int]:
        """
        The JawWorm’s action method simply returns a dictionary of
        {‘damage’:amount}.

        Parameters:
        self: The JawWorm object.

        Returns:
        Action of the JawWorm monster as a dictionary.
        """

        amount = 0
        damage_taken = self.get_max_hp() - self.get_hp()
        if damage_taken > 0:
            # rounding down the half of the amount of damage taken.
            amount = int(damage_taken // 2)

            # rounding up the half of the amount of damage taken.
            self._block += int(damage_taken // 2) + int(damage_taken % 2 == 1)
        
        actions = {"damage": amount}

        return actions

class Encounter():
    """
    Encounter manages one player and a set of 1 to 3 monsters, and
    facilitates the interactions between the player and monsters.
    """

    def __init__(self, player: Player, monsters: list[tuple[str,int]]) -> None:
        """
        The initializer for an encounter takes the player instance, as
        well as a list of tuples describing the monsters in the encounter.
        Each tuple contains the name(type) of monster and the
        monster’s max HP.

        Parameters:
        self: The encounter class object.
        player: The player object.
        monsters: 1 to 3 monsters that player needs to defeat.

        Returns:
        None.
        """

        self._is_player_turn = False
        self._player = player

        self._monsters = []
        for monster_info in monsters:
            monster_name, monster_max_hp = monster_info

            monster = None
            if monster_name == "Louse":
                monster = Louse(monster_max_hp)
            elif monster_name == "Cultist":
                monster = Cultist(monster_max_hp)
            elif monster_name == "JawWorm":
                monster = JawWorm(monster_max_hp)
            self._monsters.append(monster)

        self._player.start_new_encounter()
        self.start_new_turn()

    def start_new_turn(self) -> None:
        """
        This method sets it to be the player’s turn.

        Parameters:
        self: The encounter class object.

        Returns:
        None.
        """

        self._is_player_turn = True
        self._player.new_turn()

    def end_player_turn(self) -> None:
        """
        This method sets it to not be the player’s turn.

        Parameters:
        self: The encounter class object.

        Returns:
        None.
        """

        self._is_player_turn = False
        self._player.end_turn()
        for monster in self._monsters:
            monster.new_turn()

    def get_player(self) -> Player:
        """
        Returns the player in this encounter.

        Parameters:
        self: The encounter class object.

        Returns:
        The player object in this encounter.
        """

        return self._player

    def get_monsters(self) -> list[Monster]:
        """
        Returns the monsters remaining in this encounter.

        Parameters:
        self: The encounter class object.

        Returns:
        The list of monsters remaining in this encounter.
        """

        return self._monsters

    def is_active(self) -> bool:
        """
        Returns True if there are monsters remaining in this encounter,
        and False otherwise.

        Parameters:
        self: The encounter class object.

        Returns:
        True if monsters are remaining and False otherwise.
        """

        return self._monsters != None and len(self._monsters) > 0

    def player_apply_card(self, card_name: str,
                          target_id: int | None = None) -> bool:
        """
        This method attempts to apply the first card with the given
        name from the player’s hand.

        Parameters:
        self: The encounter class object.

        Returns:
        False for the following conditions -
            1. If it is not player's turn.
            2. If the card with the given name requires a target but no
            target was given.
            3. If a target was given but no monster remains in this
            encounter with that id.
            4. The card does not exist in the player's hand.
            5. The player does not have enough energy.
            6. The card name does not map to a card.
            
        True if the functions executes successfully.
        """

        if not self._is_player_turn:
            return False

        card = None
        for hand_card in self._player.get_hand():
            if hand_card.get_name() == card_name:
                if hand_card.requires_target() and target_id == None:
                    return False
                card = hand_card
                break

        target_monster = None
        if target_id != None:
            is_monster_available = False
            for monster in self._monsters:
                if monster.get_id() == target_id:
                    is_monster_available = True
                    target_monster = monster
                    break
            if not is_monster_available:
                return False

        if card == None or self._player.get_energy() < card.get_energy_cost():
            return False

        cards_block = card.get_block()

        status_modifiers = card.get_status_modifiers()
        cards_strength = status_modifiers.get("strength")

        self._player.add_block(cards_block)
        if cards_strength != None:
            self._player.add_strength(cards_strength)

        if card.requires_target():
            status_modifiers = card.get_status_modifiers()
            cards_weak = status_modifiers.get("weak")
            cards_vulnerable = status_modifiers.get("vulnerable")

            if cards_weak != None:
                target_monster.add_weak(cards_weak)
            if cards_vulnerable != None:
                target_monster.add_vulnerable(cards_vulnerable)

        total_damage = 0
        
        total_damage += card.get_damage_amount()
        total_damage += self._player.get_strength()

        if target_monster != None:
            if target_monster.get_vulnerable() > 0:
                total_damage = total_damage * 1.5

        if self._player.get_weak() > 0:
            total_damage = total_damage * 0.75

        total_damage = int(total_damage)

        played_card = self._player.play_card(card_name)
        if played_card != None and target_monster != None:
            target_monster.reduce_hp(total_damage)
            if target_monster.is_defeated():
                self._monsters.remove(target_monster)
        
        return True

    def enemy_turn(self) -> None:
        """
        This method attempts to allow all remaining monsters in the
        encounter to take an action.

        Parameters:
        self: The encounter class object.

        Returns:
        None
        """

        if self._is_player_turn:
            return

        for monster in self._monsters:
            effects = monster.action()

            damage_value = effects.get("damage")
            weak_value = effects.get("weak")
            vulnerable_value = effects.get("vulnerable")
            strength_value = effects.get("strength")

            if weak_value != None:
                self._player.add_weak(weak_value)
            if vulnerable_value != None:
                self._player.add_vulnerable(vulnerable_value)
            if strength_value != None:
                monster.add_strength(strength_value)

            total_damage = 0

            total_damage += damage_value
            total_damage += monster.get_strength()

            if self._player.get_vulnerable() > 0:
                total_damage = total_damage * 1.5

            if monster.get_weak() > 0:
                total_damage = total_damage * 0.75

            total_damage = int(total_damage)

            self._player.reduce_hp(total_damage)

        self.start_new_turn()

# Helper Functions
def generate_player_cards(player_name: str) -> list[Card]:
    """
    This method generates the list of cards based on the player.

    Parameters:
    player_name: Name of the player.

    Returns:
    List of cards generated for the player.
    """

    cards = []
    if player_name == "IronClad":
        cards = [Strike(), Strike(), Strike(), Strike(), Strike(),
                 Defend(), Defend(), Defend(), Defend(),
                 Bash()]
    elif player_name == "Silent":
        cards = [Strike(), Strike(), Strike(), Strike(), Strike(),
                 Defend(), Defend(), Defend(), Defend(), Defend(),
                 Neutralize(), Survivor()]
    elif player_name == "Watcher":
        cards = [Strike(), Strike(), Strike(), Strike(),
                 Defend(), Defend(), Defend(), Defend(),
                 Eruption(), Vigilance()]

    return cards

def get_card(card_name: str) -> Card:
    """
    This method instantiates the card object based on the cards name.

    Parameters:
    card_name: Name of the card.

    Returns:
    Card object based on the card name.
    """

    card = None
    if card_name == "Strike":
        card = Strike()
    elif card_name == "Defend":
        card = Defend()
    elif card_name == "Bash":
        card = Bash()
    elif card_name == "Neutralize":
        card = Neutralize()
    elif card_name == "Survivor":
        card = Survivor()
    elif card_name == "Eruption":
        card = Eruption()
    elif card_name == "Vigilance":
        card = Vigilance()

    return card

def main():
    """
    This method is used to handle the gameplay. It takes the inputs
    from the player and performs the respective actions.

    Parameters:
    None.

    Returns:
    None.
    """

    player = None
    player_type = input("Enter a player type: ")
    if player_type == "ironclad":
        player = IronClad()
    elif player_type == "silent":
        player = Silent()
    elif player_type == "watcher":
        player = Watcher()

    game_file_name = input("Enter a game file: ")
    encounters = read_game_file(game_file_name)

    player_lost = False
    for encounter in encounters:
        if not player_lost:
            encounter_obj = Encounter(player, encounter)
            print("New encounter!\n")
            display_encounter(encounter_obj)

            while True:
                player_input = input("Enter a move: ")
                
                if player_input == "end turn":
                    encounter_obj.end_player_turn()
                    encounter_obj.enemy_turn()

                    if player.get_hp() <= 0:
                        print(GAME_LOSE_MESSAGE)
                        player_lost = True
                        break

                    display_encounter(encounter_obj)
                elif player_input == "inspect deck":
                    print(f"\n{player.get_deck()}\n")
                elif player_input == "inspect discard":
                    print(f"\n{player.get_discarded()}\n")
                elif player_input[0:8].lower() == "describe":
                    card_name = player_input.split(" ", 1)[1]
                    card = get_card(card_name)
                    if card != None:
                        print(f"\n{card.get_description()}\n")
                elif player_input[0:4].lower() == "play":
                    target_id = None
                    command = player_input.split(" ")
                    card_name = command[1]
                    if len(command) == 3:
                        target_id = int(command[2])

                    result = encounter_obj.player_apply_card(card_name,\
                                                             target_id)
                    if not result:
                        print(CARD_FAILURE_MESSAGE)
                    else:
                        display_encounter(encounter_obj)

                if not encounter_obj.is_active():
                    print(ENCOUNTER_WIN_MESSAGE)
                    break

    if not player_lost:
        print(GAME_WIN_MESSAGE)

if __name__ == '__main__':
    main()
