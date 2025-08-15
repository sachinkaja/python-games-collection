import tkinter as tk
from tkinter import filedialog # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *

class InfoBar(AbstractGrid):
    """
    InfoBar inherits from Abstract Grid with 2 rows and 3 columns,
    which displays information to the user about the number of days
    elapsed in the game, as well as the player’s energy and money.
    """

    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """
        Sets up this InfoBar to be an Abstract Grid with the appropriate
        number of rows and columns, and the appropriate width and height.

        Parameters:
        master: The master widget which can be window or frame.

        Returns:
        None
        """
        
        self._master = master

        dimensions = (2,3)
        size = (FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT)

        super().__init__(self._master, dimensions, size)

    def redraw(self, day: int, money: int, energy: int) -> None:
        """
        Clears the InfoBar and redraws it to display the provided day,
        money, and energy.

        Parameters:
        day: Elapsed days to be shown on the InfoBar.
        money: Money the player has.
        energy: Energy left for the player.

        Returns:
        None
        """
        
        self.clear()
        
        self._day = day
        self._money = money
        self._energy = energy

        # Insert the text on InfoBar to specified position on the grid.
        self.annotate_position((0,0), "Day:", HEADING_FONT)
        self.annotate_position((0,1), "Money:", HEADING_FONT)
        self.annotate_position((0,2), "Energy:", HEADING_FONT)
        self.annotate_position((1,0), str(self._day))
        self.annotate_position((1,1), f"${str(self._money)}")
        self.annotate_position((1,2), str(self._energy))

class FarmView(AbstractGrid):
    """
    FarmView should inherit from AbstractGrid. The FarmView is a grid
    displaying the farmmap, player, and plants.
    """
    
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int,int],
                 size: tuple[int,int], **kwargs) -> None:
        """
        Sets up the FarmView to be an AbstractGrid with the appropriate
        dimensions and size, and creates an instance attribute of an empty
        dictionary to be used as an image cache.

        Parameters:
        master: The master widget which can be window or frame.
        dimensions: Dimensions of the grid to be set to contain the map.
        size: The pixels size of the FarmView.

        Returns:
        None
        """
        
        self._master = master
        self._dimensions = dimensions
        self._size = size
        self._image_cache = {}

        super().__init__(self._master, self._dimensions, self._size)

    def redraw(self, ground: list[str], plants: dict[tuple[int,int], 'Plant'],
               playerposition: tuple[int,int], playerdirection: str) -> None:
        """
        Clears the farmview, then creates the images for the ground,
        then the plants, then the player.

        Parameters:
        ground: The map that needs to be rendered.
        plants: The existing plants that needs to be rendered.
        playerposition: The position of the player on the grid
        as a tuple[int, int].
        playerdirection: The direction of the player (up, down, left, right).

        Returns:
        None
        """
        
        self.clear()

        cell_size = self.get_cell_size()

        # Render the ground by reading the map and insert the images
        # of Grass, Soil and Untill soil based on the map.
        for i, ground_row in enumerate(ground):
            for j, each_tile in enumerate(ground_row):
                midpoint = self.get_midpoint((i, j))
                if each_tile == GRASS:
                    image = get_image(f"images/{IMAGES.get(GRASS)}",
                                      cell_size, self._image_cache)
                elif each_tile == SOIL:
                    image = get_image(f"images/{IMAGES.get(SOIL)}",
                                      cell_size, self._image_cache)
                elif each_tile == UNTILLED:
                    image = get_image(f"images/{IMAGES.get(UNTILLED)}",
                                      cell_size, self._image_cache)
                self.create_image(midpoint, image=image)

        # Render the plants available in the plants parameter by getting
        # the image and creating it on the canvas.
        for position, plant in plants.items():
            image_path = "images/" + get_plant_image_name(plant)
            midpoint = self.get_midpoint(position)
            image = get_image(image_path, cell_size, self._image_cache)
            self.create_image(midpoint, image=image)

        # Render the player based on the player position and player
        # direction by getting the image and creating it on the canvas.
        image_path = f"images/player_{playerdirection}.png"
        midpoint = self.get_midpoint(playerposition)
        image = get_image(image_path, cell_size, self._image_cache)
        self.create_image(midpoint, image=image)

class ItemView(tk.Frame):
    """
    ItemView should inherit from tk.Frame. The ItemView is a frame displaying
    relevant information and buttons for a single item. There are 6 items
    available in the game and the widgets in the frame should align from
    left to right.
    """
    
    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """
        Sets up ItemView to operate as a tk.Frame, and creates all internal
        widgets. Sets the commands for the buy and sell buttons to the
        buy_command and sell_command each called with the appropriate
        item_name respectively. Binds the select_command to be called with the
        appropriate item_name when either the ItemView frame or label
        is left clicked.

        Parameters:
        master: The master widget which is a frame.
        item_name: Name of the item.
        amount: Available inventory for the item.
        select_command: Binding the selection of item function.
        sell_command: Binding the buying of an item function.
        buy_command: Binding the selling of an item function.

        Returns:
        None
        """
        
        self._master = master
        self._item_name = item_name
        self._amount = amount
        self._select_command = select_command
        self._sell_command = sell_command
        self._buy_command = buy_command
        self._selected = False

        super().__init__(self._master)

        # Label creation for the item view which has the item name,
        # sell price and buy price of the item.
        self._sell_price = SELL_PRICES.get(item_name)
        self._buy_price = BUY_PRICES.get(item_name)
        if self._buy_price == None:
            self._buy_price = 'N/A'

        item_name_text = f"{self._item_name}: {str(self._amount)}"
        sell_text = f"Sell price: ${str(self._sell_price)}"
        buy_text = f"Buy price: ${str(self._buy_price)}"
        info_text = f"{item_name_text}\n{sell_text}\n{buy_text}"

        self._information = tk.Label(
            self,
            text=info_text,
            padx=10
        )
        self._information.pack(
            side=tk.LEFT
        )

        # Buy Button creation for the item view if buy price is available
        if str(self._buy_price) != 'N/A':
            self._buy = tk.Button(
                self,
                text="Buy",
                padx=10,
                command = (
                    lambda: self._buy_command(item_name)
                    if self._buy_command
                    else None
                )
            ).pack(
                side=tk.LEFT
            )
        
        # Sell Button creation for the item view
        self._sell = tk.Button(
            self,
            text="Sell",
            padx=10,
            command = (
                lambda: self._sell_command(item_name)
                if self._sell_command
                else None
            )
        ).pack(
            side=tk.LEFT
        )

        self.pack(expand=tk.TRUE, fill=tk.BOTH)

        # Binding the select command to the frame and label for changing
        # the text and color on selection of the item.
        self.bind(
            "<Button-1>",
            lambda event: self._select_command(item_name)
            if self._select_command
            else None
        )
        self._information.bind(
            "<Button-1>",
            lambda event: self._select_command(item_name)
            if self._select_command
            else None
        )

        self.update(self._amount)

    def update(self, amount: int, selected: bool = False) -> None:
        """
        Updates the text on the label, and the colour of this ItemView
        appropriately.

        Parameters:
        amount: Amount to be updated on the item text.
        selected: Boolean value which represents if the item is selected.

        Returns:
        None
        """
        
        self._amount = amount
        self._selected = selected

        item_name_text = f"{self._item_name}: {str(amount)}"
        sell_text = f"Sell price: ${str(self._sell_price)}"
        buy_text = f"Buy price: ${str(self._buy_price)}"
        info_text = f"{item_name_text}\n{sell_text}\n{buy_text}"

        # update the amount in the label withthe given amount.
        self._information.config(text=info_text)

        # update the color for the frame and label based on available
        # inventory and selection of the item.
        bg_color = ""
        if self._amount == 0:
            bg_color = INVENTORY_EMPTY_COLOUR
        else:
            if self._selected:
                bg_color = INVENTORY_SELECTED_COLOUR
            else:
                bg_color = INVENTORY_COLOUR

        self.config(bg=bg_color,
                    highlightbackground=INVENTORY_OUTLINE_COLOUR,
                    highlightthickness=1)
        self._information.config(bg=bg_color)

class FarmGame():
    """
    FarmGame is the controller class for the overall game. The controller
    is responsible for creating and maintaining instances of the model and
    view classes, event handling, and facilitating communication between the
    model and view classes.
    """
    
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        Sets the title of the window, a title banner to have the header image,
        creates the FramModel instance, creates the instances of all the view
        classes, creates the next day button, handles the keypress method, and
        calls the redraw method to refresh the view classes.

        Parameters:
        master: The master widget which is the root window.
        map_file: The map that should be loaded to the FarmView instance.

        Returns:
        None
        """
        
        self._master = master
        self._map_file = map_file
        self._cache = {}

        self._master.title("Farm Game")

        # TITLE BANNER having the header image.
        title_frame = tk.Frame(
            self._master
        )
        title_frame.pack()

        image_path = "images/header.png"
        banner_size = (FARM_WIDTH + INVENTORY_WIDTH, BANNER_HEIGHT)
        title_image = get_image(image_path, banner_size, self._cache)
        tk.Label(
            title_frame,
            image=title_image
        ).pack()

        # Creation of FarmModel instance.
        self._farmModel = FarmModel(self._map_file)

        # Creayion of frame for FarmView and ItemViews.
        self._farm_item_frame = tk.Frame(
            self._master
        )
        self._farm_item_frame.pack()
        
        # Creation of Farm View Instance
        self.create_farmview()

        # Creation of Item View Instances
        self.create_itemviews()

        # Creation ofInfoBar Instance
        infobar_frame = tk.Frame(
            self._master
        )
        infobar_frame.pack()
        
        self._inforBar = InfoBar(infobar_frame)
        self._inforBar.pack()

        # Creation ofNext Day Button
        next_day = tk.Button(
            self._master,
            text="Next day",
            padx=10,
            command=self.next_day_click
        )
        next_day.pack(
            side=tk.BOTTOM
        )

        # Binding the <KeyPress> on the FarmGame master.
        self._master.bind('<KeyPress>', self.handle_keypress)

        # Creating the menu with Quit and Map selection options.
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Quit", command=self.quit)
        filemenu.add_command(label="Map selection", command=self.map_selection)

        self.redraw()

    def redraw(self) -> None:
        """
        Redraws the entire game based on the current model state.

        Parameters:
        self: The FarmGame instance.

        Returns:
        None
        """
        
        # redraw InfoBar with updated infomartion.
        day = self._farmModel.get_days_elapsed()
        money = self._farmModel.get_player().get_money()
        energy = self._farmModel.get_player().get_energy()

        self._inforBar.redraw(day, money, energy)

        # redraw FarmView with updated infomartion.
        ground = self._farmModel.get_map()
        plants = self._farmModel.get_plants()
        player_position = self._farmModel.get_player_position()
        player_direction = self._farmModel.get_player_direction()

        self._farmView.redraw(ground, plants,
                              player_position, player_direction)

        # update ItemViews with updated infomartion.
        for item_view in self._item_views:
            item_name = item_view._item_name
            player_inventory = self._farmModel.get_player().get_inventory()
            amount = player_inventory.get(item_name)
            if amount == None:
                amount = 0

            item_view.update(amount)

    def handle_keypress(self, event: tk.Event) -> None:
        """
        An event handler to be called when a key press event occurs.

        Parameters:
        event: The key press event.

        Returns:
        None
        """
        
        if event.char == UP:
            # Move the player UP.
            self._farmModel.move_player(UP)
        elif event.char == DOWN:
            # Move the player DOWN.
            self._farmModel.move_player(DOWN)
        elif event.char == LEFT:
            # Move the player LEFT.
            self._farmModel.move_player(LEFT)
        elif event.char == RIGHT:
            # Move the player RIGHT
            self._farmModel.move_player(RIGHT)
        elif event.char == "p":
            # Plant the seed at the player position and redraw the views.
            selected_item_name = ""
            item_amount = 0

            # Get the item name and amount of the selected item
            for item_view in self._item_views:
                if item_view._selected:
                    selected_item_name = item_view._item_name
                    item_amount = item_view._amount

            # Proceed only if the item is a seed and amount is greater than 0.
            if selected_item_name in SEEDS and item_amount > 0:
                player_position = self._farmModel.get_player_position()
                row, col = player_position
                # Proceed only if the player is on the soil.
                if (self._farmModel.get_map()[row][col] == UNTILLED
                            or self._farmModel.get_map()[row][col] == SOIL):
                    # Create the plant instance with the given item name.
                    plant = self.create_plant(selected_item_name.split(" ")[0])

                    if self._farmModel.add_plant(player_position, plant):
                        to_remove = (selected_item_name, 1)
                        self._farmModel.get_player().remove_item(to_remove)
        elif event.char == "h":
            # Harvest the plant from player position if possible.
            to_add = self._farmModel.harvest_plant(
                self._farmModel.get_player_position())
            if to_add:
                self._farmModel.get_player().add_item(to_add)
        elif event.char == "r":
            # Remove the plant from player position if available.
            self._farmModel.remove_plant(self._farmModel.get_player_position())
        elif event.char == "t":
            # Till the soil on the player position.
            self._farmModel.till_soil(self._farmModel.get_player_position())
        elif event.char == "u":
            # Untill the soil on the player position.
            self._farmModel.untill_soil(self._farmModel.get_player_position())

        self.redraw()

    def select_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView for item selection.
        This method should set the selected item to be item_name and then
        redraw the view.

        Parameters:
        item_name: Name of the item selected.

        Returns:
        None
        """
        
        # Iterate through ItemViews and update the amount in the label
        # and color for the frame and label based on the selection.
        for item_view in self._item_views:
            if item_view._item_name == item_name:
                item_view.update(item_view._amount, True)
            else:
                item_view.update(item_view._amount, False)

    def buy_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView for buying items. This
        method should cause the player to attempt to buy the item with the
        given item_name, at the price specified in BUY_PRICES, and then
        redraw the view.

        Parameters:
        item_name: Name of the item selected.

        Returns:
        None
        """
        
        # Proceed to buy the item if item buy price is available.
        if item_name in BUY_PRICES:
            amount = BUY_PRICES.get(item_name)
            self._farmModel.get_player().buy(item_name, amount)
        self.redraw()

    def sell_item(self, item_name: str) -> None:
        """
        The callback to be given to each ItemView for selling items. This
        method should cause the player to attempt to sell the item with the
        given item_name, at the price specified in SELL_PRICES, and then
        redraw the view.

        Parameters:
        item_name: Name of the item selected.

        Returns:
        None
        """
        
        # Proceed to sell the item if item sell price is available.
        if item_name in SELL_PRICES:
            amount = SELL_PRICES.get(item_name)
            self._farmModel.get_player().sell(item_name, amount)
        self.redraw()

    def next_day_click(self) -> None:
        """
        Increments the day and redraws the entire view classes.

        Parameters:
        self: FarmGame instance.

        Returns:
        None.
        """

        # New day method will update the information and redraw the views.
        self._farmModel.new_day()
        self.redraw()

    def create_farmview(self) -> None:
        """
        Method to create the FramView instance.

        Parameters:
        self: FarmGame instance.

        Returns:
        None.
        """
        
        dimensions = self._farmModel.get_dimensions()
        size = (FARM_WIDTH, FARM_WIDTH)
        
        self._farmView = FarmView(self._farm_item_frame, dimensions, size)
        self._farmView.pack(
            side=tk.LEFT
        )

    def create_itemviews(self) -> None:
        """
        Method to create all the ItemView instances for 6 items.

        Parameters:
        self: FarmGame instance.

        Returns:
        None.
        """
        
        self._item_views = []
        for item_name in ITEMS:
            player_inventory = self._farmModel.get_player().get_inventory()
            amount = player_inventory.get(item_name)
            if amount == None:
                amount = 0

            # Store the newly created ItemView instances in a list.
            self._item_views.append(ItemView(self.make_item_frame(),
                                       item_name, amount, self.select_item,
                                       self.sell_item, self.buy_item))

    def make_item_frame(self) -> tk.Frame:
        """
        Creates an item frame which can be used for each item in ItemView.

        Parameters:
        self: FarmGame instance.

        Returns:
        tk.Frame: Returns the created frame.
        """
        
        item_frame = tk.Frame(
            self._farm_item_frame,
            width=INVENTORY_WIDTH
        )
        item_frame.pack(
            side=tk.TOP,
            expand=tk.TRUE,
            fill=tk.BOTH
        )
        
        return item_frame

    def create_plant(self, plant_name: str) -> Plant:
        """
        Creates a plant instance with the given name.

        Parameters:
        plant_name: Name of the plant to be created.

        Returns:
        Plant: Returns the created plant instance.
        """
        
        plant = None
        if plant_name == "Potato":
            plant = PotatoPlant()
        elif plant_name == "Kale":
            plant = KalePlant()
        elif plant_name == "Berry":
            plant = BerryPlant()

        return plant

    def quit(self) -> None:
        """
        Closes the complete game by destroy method.

        Parameters:
        self: FarmGame instance.

        Returns:
        None.
        """
        
        self._master.destroy()

    def map_selection(self) -> None:
        """
        Selects the new map from the file dialog and redraws the
        complete game.

        Parameters:
        self: FarmGame instance.

        Returns:
        None.
        """
        
        # Get the directory of the chosen map file.
        name = filedialog.askopenfilename()

        # Proceed only if a map file is selected.
        if name:
            name_components = name.split("/")[-2:]
            self._map_file = name_components[0] + "/" + name_components[1]
            self._farmModel = FarmModel(self._map_file)

            # Destroy the FarmView and ItemViews frame and redraw with new map.
            for each_widget in self._farm_item_frame.winfo_children():
                each_widget.destroy()

            self.create_farmview()
            self.create_itemviews()
            
            self.redraw()

def play_game(root: tk.Tk, map_file: str) -> None:
    """
    Constructs the controller instance (FarmGame) with the given map_file
    and the root window parameters.

    Parameters:
    root: tk.Tk instance - root window.
    map_file: The selected map for the game.

    Returns:
    None.
    """
    
    farmGame = FarmGame(root, map_file)
    root.mainloop()

def main() -> None:
    """
    Constructs the root tk.Tk instance and calls the play_game function
    by passing the created root instance and the map selected for the game.

    Parameters:
    None.

    Returns:
    None.
    """
    
    root = tk.Tk()
    map_file = "maps/map1.txt"
    play_game(root, map_file)

if __name__ == '__main__':
    main()
