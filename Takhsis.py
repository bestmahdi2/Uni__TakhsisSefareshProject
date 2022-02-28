import enum
import re
from typing import Union, Tuple
import tkinter as tk
import tkinter.font as tk_font
from functools import partial


class ServiceCategory(enum.Enum):
    """
       Enum class for ServiceCategory.
    """
    BIKE = "BIKE"
    VAN = "VAN"
    TRUCK = "TRUCK"


class DriverStatus(enum.Enum):
    """
       Enum class for DriverStatus.
    """
    FREE = "FREE"
    BUSY = "BUSY"


class OrderStatus(enum.Enum):
    """
       Enum class for OrderStatus.
    """
    PENDING = "PENDING"
    ARRIVED = "ARRIVED"
    PICKUP = "PICKUP"
    DELIVERED = "DELIVERED"


class Tools:
    """
       This is a class for helping other classes to use same functions.
    """

    @staticmethod
    def position_str2tuple(position: str) -> Union[Tuple[int, ...], bool]:
        """
        The function to convert string to tuple.
        If string is not valid:
            returns False

        Parameters:
            position (str): The string value of position

        Returns:
            False: if not any match in case,
            Tuple: tuple value of string position.
        """
        reg = r"^\(-?[0-9]+, -?[0-9]+\)$"

        if re.match(reg, position):
            return tuple([int(i) for i in position.replace("(", "").replace(")", "").split(", ")])
        else:
            return False

    @staticmethod
    def find_distance_all_tuple(first: tuple, second: tuple) -> int:
        """
        The function find the distance between two tuple.

        Parameters:
            first (tuple): The tuple value of first position.
            second (tuple): The tuple value of second position.

        Returns:
            int : A integer value of |x1 - y1| + |x2 - y2|
        """
        return abs(first[0] - second[0]) + abs(first[1] - second[1])

    @staticmethod
    def find_distance(first: tuple, second: str) -> int:
        """
        The function find the distance between two position,
        It first converts string value to tuple.

        Parameters:
            first (tuple): The tuple value of first position.
            second (str): The string value of second position.

        Returns:
            int : A integer value of |x1 - y1| + |x2 - y2|
        """

        second = Tools.position_str2tuple(second)
        return abs(first[0] - second[0]) + abs(first[1] - second[1])


class Command:
    """
       This is a class for getting commands and stating the program.
    """

    def __init__(self):
        """
           Constructor function,

           self.drivers: list to keep all drivers added to program.
           self.orders: list to keep all orders added to program.
           self.order_for_drivers: list to keep all drivers + their orders.
           self.order_count: int to keep orders added to program till now.
           self.company_profit: list to keep company profit.
        """
        self.drivers = []
        self.orders = []
        self.order_for_drivers = {}
        self.order_count = 0
        self.company_profit = 0

    def main(self, gui: bool = False, inputs: list = []):
        """
           main function,

           self.drivers: list to keep all drivers added to program.
           self.orders: list to keep all orders added to program.
           self.order_for_drivers: list to keep all drivers + their orders.
           self.order_count: int to keep orders added to program till now.
           self.company_profit: list to keep company profit.
        """

        if not gui:
            while True:
                inputer = input()
                if inputer == "END":
                    break

                inputs.append(inputer)

        for command in inputs:
            command = command.split(" ")
            result = ""

            if command[0] == "ADD-DRIVER":
                result = self.add_driver(command[1:])

            elif command[0] == "CREATE-ORDER":
                result = self.create_order(command[1:])

            elif command[0] == "ASSIGN-NEXT-ORDER":
                result = self.assign_next_order(command[1:])

            elif command[0] == "GET-DRIVER":
                result = self.get_driver(command[1:])

            elif command[0] == "ORDER-UPDATE":
                result = self.order_update(command[1:])

            elif command[0] == "GET-ORDER":
                result = self.get_order(command[1:])

            elif command[0] == "GET-ORDER-LIST":
                result = self.get_order_list(command[1:])

            elif command[0] == "GET-DRIVER-LIST":
                result = self.get_driver_list(command[1:])

            elif command[0] == "GET-NEAR-DRIVER":
                result = self.get_near_driver(command[1:])

            elif command[0] == "GET-CNT-ORDER":
                result = self.get_cnt_order(command[1:])

            elif command[0] == "GET-NEAREST-PENDING-ORDER":
                result = self.get_nearest_pending_order(command[1:])

            elif command[0] == "GET-COMPANY":
                result = self.get_company()

            if gui:
                return result

            print(result)

    def add_driver(self, info: list) -> str:
        """
        The function to add a new driver to program,
        If driver is not already signed up, it creates a new object from Driver and adds it to drivers, also
        it creates a new driver in order_for_driver and sets it to an empty list.

        Parameters:
            info (list): All needed info to create a new driver.
        """

        username, position, service_category = info[0], " ".join(info[1:3]), info[3]

        if username in self.order_for_drivers:
            return "user previously added"

        else:
            driver = Driver(username, [i for i in ServiceCategory if i.value == service_category][0], position,
                            DriverStatus.FREE)

            self.drivers.append(driver)
            if username not in self.order_for_drivers:
                self.order_for_drivers[username] = []

            return "user added successfully"

    def create_order(self, info: list) -> str:
        """
        The function to add a new order to program,
        If start position and finish position aren't equal, it creates a new object from Order and adds it to orders.

        Parameters:
            info (list): All needed info to create a new order.
        """

        service_category, starting_position, finishing_position = info[0], " ".join(info[1:3]), " ".join(info[3:])

        if info[1] == info[2]:
            return "invalid order"

        else:
            self.order_count += 1
            order = Order([i for i in ServiceCategory if i.value == service_category][0], starting_position,
                          finishing_position, self.order_count, OrderStatus.PENDING, self.orders)

            self.orders.append(order)
            return str(order.order_id)

    def assign_next_order(self, username: list) -> str:
        """
        The function to assign the next order to driver whom username's given.
        It finds driver and available orders and assign the closest order to the driver in case of no problem,

        Parameters:
            username (list): Username of the driver to be assigned to new order.
        """

        username = username[0]

        # find driver which its username is equal to this username
        driver = [i for i in self.drivers if i.username == username][0]
        # find orders which are Pending and their service_category is same as driver's.
        orders = [i for i in self.orders if
                  i.status == OrderStatus.PENDING and i.service_category == driver.service_category]

        if username not in self.order_for_drivers:
            return "invalid driver name"

        elif driver.status == DriverStatus.BUSY:
            return "driver is already busy"

        elif len(orders) == 0:
            return "there is no order right now"

        else:
            # sort orders by finding their distance to driver > then their id
            orders = sorted(orders,
                            key=lambda order: (Tools.find_distance_all_tuple(driver.position, order.starting_position),
                                               order.order_id))

            # change order status
            for i in range(len(self.orders)):
                if self.orders[i] == orders[0]:
                    self.orders[i].status = OrderStatus.ARRIVED
                    break

            # change driver status
            for i in range(len(self.drivers)):
                if self.drivers[i] == driver:
                    self.drivers[i].status = DriverStatus.BUSY
                    break

            # add order to driver's order list in order_for_drivers
            self.order_for_drivers[username].append(orders[0])

            return f"{orders[0].order_id} assigned to {username}"

    def get_driver(self, username: list) -> str:
        """
        The function to get a driver information.
        Parameters:
            username (list): Username of the driver to be assigned to new order.
        """

        username = username[0]

        if username not in self.order_for_drivers:
            return "invalid driver name"

        else:
            # find driver in drivers by its username
            driver = [i for i in self.drivers if i.username == username][0]
            return f"{driver.status.value} {driver.position} {int(driver.credit)}"

    def order_update(self, info: list) -> str:
        """
        The function to update an order.
        If there is no problem, it finds order and driver and change their status, credit, position in each condition.

        Parameters:
            info (list): information needed to update an order.
        """

        order_status_list = [e.value for e in OrderStatus]
        status, username, order_id = [i for i in OrderStatus if i.value == info[0]][0], info[1], int(info[2])
        order = [i for i in self.orders if i.order_id == order_id]  # find order
        driver = [i for i in self.drivers if i.username == username]  # find driver

        if username not in self.order_for_drivers:
            return "invalid driver name"

        elif order_id not in [i.order_id for i in self.order_for_drivers[username]]:
            return "wrong order-id"

        elif order_status_list.index(order[0].status.value) > order_status_list.index(status.value):
            return "invalid status"

        else:
            # change order status no matter what new value is.
            for i in range(len(self.orders)):
                if self.orders[i] == order[0]:
                    self.orders[i].status = status
                    break

            # change credit, status and position of driver (and company profit) if order is delivered.
            if status == OrderStatus.DELIVERED:
                for i in range(len(self.drivers)):
                    if self.drivers[i] == driver[0]:
                        self.drivers[i].credit = order[0].cost
                        self.drivers[i].status = DriverStatus.FREE
                        self.drivers[i].position = order[0].finishing_position
                        break

                self.company_profit += 0.2 * order[0].cost

            # change position of driver if order is picked up
            if status == OrderStatus.PICKUP:
                for i in range(len(self.drivers)):
                    if self.drivers[i] == driver[0]:
                        self.drivers[i].position = order[0].starting_position
                        break

            return "status changed successfully"

    def get_order(self, order_id: list) -> str:
        """
        The function to find information of an order by its id.

        Parameters:
            order_id (list): order id to get information of order.
        """

        order_id = int(order_id[0])
        order = [i for i in self.orders if i.order_id == order_id]  # find order by order_id

        if not order:
            return "invalid order"

        else:
            # find order's driver
            driver_username = [i for i in self.order_for_drivers if order[0] in self.order_for_drivers[i]]

            if driver_username:
                return f"{order[0].status.value} {driver_username[0]} {order[0].cost}"

            else:
                return f"{order[0].status.value} None {order[0].cost}"

    def get_order_list(self, status: list) -> str:
        """
        The function to get list of all orders with status given.

        Parameters:
            status (list): status of orders.
        """

        status = status[0]
        wanted_status_list = [i.order_id for i in self.orders if i.status.value == status]

        if wanted_status_list:
            return " ".join([str(i) for i in wanted_status_list])

        else:
            return "None"

    def get_driver_list(self, status: list) -> str:
        """
        The function to get list of all drivers with status given.

        Parameters:
            status (list): status of drivers.
        """

        status = status[0]
        wanted_driver_list = [i.username for i in self.drivers if i.status.value == status]

        if wanted_driver_list:
            return " ".join(wanted_driver_list)

        else:
            return "None"

    def get_near_driver(self, info: list) -> str:
        """
        The function to find nearest drivers to a given position.

        Parameters:
            info (list): information needed for getting nearest drivers.
        """

        position, count = " ".join(info[:2]), int(info[2])
        # find free drivers
        free_drivers = list(set([i for i in self.drivers if i.status.value == "FREE"]))

        # sort drivers by finding their distance to given position > then their order of adding to program.
        free_drivers = sorted(free_drivers, key=lambda driver: (Tools.find_distance(driver.position, position),
                                                                self.drivers.index(driver)))

        if len(free_drivers) <= count:
            return " ".join([i.username for i in free_drivers])

        elif len(free_drivers) > count:
            return " ".join([i.username for i in free_drivers][:count])

        else:
            return "None"

    def get_cnt_order(self, info: list) -> str:
        """
        The function to get number of orders which are in distance from given position at maximum.

        Parameters:
            info (list): information needed for getting number of orders.
        """

        position, distance, mode = " ".join(info[0:2]), int(info[2]), info[3]

        if mode == "START":
            orders = [i for i in self.orders if Tools.find_distance(i.starting_position, position) <= distance]

        else:
            orders = [i for i in self.orders if Tools.find_distance(i.finishing_position, position) <= distance]

        return str(len(orders))

    def get_nearest_pending_order(self, position: list) -> str:
        """
        The function to find nearest pending order to position given.

        Parameters:
            position (list): the position of order to be checked.
        """

        position = " ".join(position[0:2])
        orders = [i for i in self.orders if i.status == OrderStatus.PENDING]  # get pending orders

        if orders:
            # sort orders by finding their distance to position
            orders = sorted(orders, key=lambda order: Tools.find_distance(order.starting_position, position))
            return str(orders[0].order_id)

        else:
            return "None"

    def get_company(self) -> str:
        """
        The function to get company profit.
        """

        return str(int(self.company_profit))


class Driver:
    """
       This is a class for simulating a Driver.

       Attributes:
            username (str): The string value of new username
            service_category (ServiceCategory): The ServiceCategory value of new service_category
            position (str): The string value of position in (x, y)
            status (DriverStatus): The DriverStatus value of new status
       """

    def __init__(self, username: str, service_category: ServiceCategory, position: str, status: DriverStatus) -> None:
        """
        Constructor function,

        Parameters:
            username (str): The string value of new username
            service_category (ServiceCategory): The ServiceCategory value of new service_category
            position (str): The string value of position in (x, y)
            status (DriverStatus): The DriverStatus value of new status
        """
        self.username = username
        self.service_category = service_category
        self._credit = 0
        self.position = position
        self.status = status

    @property
    def username(self) -> str:
        """
        Username getter function

        Returns:
            self._username: A string value of username
        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """
        The function to set username of a driver,
        Also checks if :
            username is not empty
            username length is not more than 25
            username contains only digit and alphabetical characters

        Parameters:
            username (str): The string value of new username
        """
        for char in username:
            if not username:
                print("Username can't be empty !")
                break
            elif len(username) > 25:
                print("Username characters is more than 25 !")
                break
            elif not char.isdigit() and not char.isalpha():
                print("Username must contain only digit and alphabetical characters !")
                break
        else:
            self._username = username

    @property
    def service_category(self) -> ServiceCategory:
        """
        Service category getter function

        Returns:
            self._service_category: A ServiceCategory object of service_category
        """
        return self._service_category

    @service_category.setter
    def service_category(self, service_category: ServiceCategory):
        """
        The function to set service category of a driver,

        Parameters:
            service_category (ServiceCategory): The ServiceCategory value of new service_category
        """
        self._service_category = service_category

    @property
    def credit(self) -> int:
        """
        Credit getter function

        Returns:
            self._credit: A integer value of credit
        """
        return self._credit

    @credit.setter
    def credit(self, cost: int):
        """
        The function to set credit of a driver,

        Parameters:
            cost (int): The cost the package driver delivers
        """
        self._credit = cost * 0.8

    @property
    def position(self) -> tuple:
        """
        Position getter function

        Returns:
            self._position: A tuple value of position in (x, y)
        """
        return self._position

    @position.setter
    def position(self, position) -> None:
        """
        The function to set position of a driver,
        If position type is string:
            use Tools.position_str2tuple()

        Parameters:
            position (str/tuple): The string/tuple value of position in (x, y)
        """
        if type(position) == str:
            if Tools.position_str2tuple(position):
                self._position = Tools.position_str2tuple(position)
        else:
            self._position = position

    @property
    def status(self) -> DriverStatus:
        """
        Status getter function

        Returns:
            self._status: A DriverStatus object of status
        """
        return self._status

    @status.setter
    def status(self, status: DriverStatus) -> None:
        """
        The function to set status of a driver,

        Parameters:
            status (DriverStatus): The DriverStatus value of new status
        """
        self._status = status


class Order:
    """
       This is a class for simulating a Order.

       Attributes:
            service_category (ServiceCategory): The ServiceCategory value of new service_category
            starting_position (str): The string value of starting position in (x, y)
            finishing_position (str): The string value of finishing position in (x, y)
            order_id (int): The integer value of order's id
            status (OrderStatus): The OrderStatus object of status
            orders (list): The list of previous orders
    """

    def __init__(self, service_category: ServiceCategory, starting_position: str, finishing_position: str,
                 order_id: int, status: OrderStatus, orders: list) -> None:
        """
        Constructor function,

        Parameters:
            service_category (ServiceCategory): The ServiceCategory value of new service_category
            starting_position (str): The string value of starting position in (x, y)
            finishing_position (str): The string value of finishing position in (x, y)
            order_id (int): The integer value of order's id
            status (OrderStatus): The OrderStatus object of status
            orders (list): The list of previous orders
        """
        self.orders = orders
        self.service_category = service_category
        self.starting_position = starting_position
        self.finishing_position = finishing_position
        self.cost = [self._starting_position, self._finishing_position]
        self.order_id = order_id
        self.status = status

    @property
    def service_category(self) -> ServiceCategory:
        """
        Service category getter function

        Returns:
            self._service_category: A ServiceCategory value of service_category
        """
        return self._service_category

    @service_category.setter
    def service_category(self, service_category: ServiceCategory):
        """
        The function to set service category of an order,

        Parameters:
            service_category (ServiceCategory): The ServiceCategory value of new service_category
        """
        self._service_category = service_category

    @property
    def starting_position(self) -> tuple:
        """
        Starting position getter function

        Returns:
            self._starting_position: A tuple value of starting position
        """
        return self._starting_position

    @starting_position.setter
    def starting_position(self, starting_position: str) -> None:
        """
        The function to set starting position of an order,
        It changes string to tuple.

        Parameters:
            starting_position (str): The string value of new starting position
        """
        if Tools.position_str2tuple(starting_position):
            self._starting_position = Tools.position_str2tuple(starting_position)

    @property
    def finishing_position(self) -> tuple:
        """
        Finishing position getter function

        Returns:
            self._finishing_position: A tuple value of finishing position
        """
        return self._finishing_position

    @finishing_position.setter
    def finishing_position(self, finishing_position: str) -> None:
        """
        The function to set finishing position of an order,
        It changes string to tuple.

        Parameters:
            finishing_position (str): The string value of new finishing position
        """
        if Tools.position_str2tuple(finishing_position):
            self._finishing_position = Tools.position_str2tuple(finishing_position)

    @property
    def cost(self) -> int:
        """
        Cost getter function

        Returns:
            self._cost: A int value of cost of order
        """
        return self._cost

    @cost.setter
    def cost(self, positions: list):
        """
        The function to find cost of the order,
        find k with length of all Pending orders which have same service category

        Parameters:
            positions (list): The list value of new starting and finishing positions
        """
        starting_position, finishing_position = positions[0], positions[1]
        k = len(
            [i for i in self.orders if i.status == OrderStatus.PENDING and i.service_category == self.service_category])

        self._cost = (k + 1 + Tools.find_distance_all_tuple(starting_position, finishing_position)) * 100

    @property
    def order_id(self) -> int:
        """
        Order ID getter function

        Returns:
            self._order_id: A int value of order's id
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id: int):
        """
        The function to set order_id of the order,

        Parameters:
            order_id (int): The int value of order_id
        """
        self._order_id = order_id

    @property
    def status(self) -> OrderStatus:
        """
        Order ID getter function

        Returns:
            self._order_id: A int value of order's id
        """
        return self._status

    @status.setter
    def status(self, status: OrderStatus):
        """
        The function to set status of the order,

        Parameters:
            status (OrderStatus): The OrderStatus value of status
        """
        self._status = status


class GraphicalMenu:
    """
        This is a class for gui use.

        Arguments:
            root (tk): root frame of application
    """

    def __init__(self, root):
        """
           Constructor function,

            Parameters:
                root : root frame of application
        """
        # object from Command class
        self.command = Command()

        # initialize labels
        label_select = tk.Label(root, font=tk_font.Font(family='Calibri Bold', size=20), fg="#FDF5E6", bg="#569FE7",
                                justify="center", text="Select your command from below")

        self.label_mode = tk.Label(root, borderwidth=2, relief="groove",
                                   font=tk_font.Font(family='Calibri Bold', size=11), fg="#FDF5E6", bg="#569FE7",
                                   justify="center", text="Mode")

        self.message_show_result = tk.Label(root, font=tk_font.Font(family='Calibri bold', size=15), fg="#F4CA16",
                                            bg="#569FE7", justify="center")

        label_select.place(x=10, y=10, width=580, height=56)
        self.label_mode.place(x=30, y=300, width=150, height=50)
        self.message_show_result.place(x=30, y=410, width=540, height=55)

        # initialize lineEdit
        self.lineEdit = tk.Entry(root, borderwidth="1px", font=tk_font.Font(family='Calibri', size=15), fg="black")
        self.lineEdit.place(x=200, y=300, width=370, height=50)

        # initialize buttons, same properties were set to variables
        bg = "#CC397B"
        fg = "#ffffff"
        font = tk_font.Font(family='Calibri bold', size=10)
        width = 100
        height = 50

        # region button
        GraphicalMenu.Button(root, bg, fg, font, "ADD-DRIVER", {'x': 30, 'y': 90, 'w': width, 'h': height},
                             partial(self.commander, "ADD-DRIVER"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-DRIVER", {'x': 140, 'y': 90, 'w': width, 'h': height},
                             partial(self.commander, "GET-DRIVER"))

        GraphicalMenu.Button(root, bg, fg, font, "ASSIGN-NEXT-\nORDER", {'x': 250, 'y': 90, 'w': width, 'h': height},
                             partial(self.commander, "ASSIGN-NEXT-ORDER"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-DRIVER-LIST", {'x': 360, 'y': 90, 'w': width, 'h': height},
                             partial(self.commander, "GET-DRIVER-LIST"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-NEAR-DRIVER", {'x': 470, 'y': 90, 'w': width, 'h': height},
                             partial(self.commander, "GET-NEAR-DRIVER"))

        GraphicalMenu.Button(root, bg, fg, font, "CREATE-ORDER", {'x': 30, 'y': 160, 'w': width, 'h': height},
                             partial(self.commander, "CREATE-ORDER"))

        GraphicalMenu.Button(root, bg, fg, font, "ORDER-UPDATE", {'x': 140, 'y': 160, 'w': width, 'h': height},
                             partial(self.commander, "ORDER-UPDATE"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-ORDER", {'x': 250, 'y': 160, 'w': width, 'h': height},
                             partial(self.commander, "GET-ORDER"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-ORDER-LIST", {'x': 360, 'y': 160, 'w': width, 'h': height},
                             partial(self.commander, "GET-ORDER-LIST"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-CNT-ORDER", {'x': 470, 'y': 160, 'w': width, 'h': height},
                             partial(self.commander, "GET-CNT-ORDER"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-NEAREST-\nPENDING-\nORDER",
                             {'x': 30, 'y': 230, 'w': width, 'h': height},
                             partial(self.commander, "NEAREST-PEND-ORDER"))

        GraphicalMenu.Button(root, bg, fg, font, "GET-COMPANY", {'x': 140, 'y': 230, 'w': width, 'h': height},
                             self.get_company)

        GraphicalMenu.Button(root, "#50C878", fg, font, "Get Result", {'x': 500, 'y': 370, 'w': 70, 'h': 30},
                             self.button_get_result_command)

        # endregion

    @staticmethod
    def Button(root, bg: str, fg: str, font: tk_font.Font, text: str, place: dict, command, justify: str = "center",
               relief: str = "flat") -> tk.Button:
        """
        The function to create and return a new TK button

        Parameters:
            root : root frame of application
            bg (str): background color
            fg (str): foreground color
            font (tk_font.Font): font of the button's text
            text (str): text of the button
            place (dict): position of the button
            command : the function with its parameter
            justify (str): button text justify
            relief (str): relief of the button

        Returns:
            temp_button: A tk.Button object of button created with given information
        """

        temp_button = tk.Button(root, relief=relief, cursor="hand2")
        temp_button["bg"] = bg
        temp_button["font"] = font
        temp_button["fg"] = fg
        temp_button["justify"] = justify
        temp_button["text"] = text
        temp_button.place(x=place['x'], y=place['y'], width=place['w'], height=place['h'])
        temp_button["command"] = command

        return temp_button

    def commander(self, command: str) -> None:
        """
        The function to clear lineEdit and message_show_result and set command's text to label_mode

        Parameters:
            command (str): The command user clicked on
        """

        self.lineEdit.delete(0, "end")
        self.message_show_result["text"] = ""
        self.label_mode["text"] = command

    def get_company(self) -> None:
        """
        The function for GET-COMPANY button
        """

        self.lineEdit.delete(0, "end")
        self.lineEdit.insert(0, "---")
        self.label_mode["text"] = "GET-COMPANY"

        try:
            self.message_show_result["text"] = self.command.main(True, ["GET-COMPANY"])

        except Exception:
            self.message_show_result["text"] = "Wrong entrance !"

    def button_get_result_command(self) -> None:
        """
        The function for getting results of the command user clicked and wrote
        """

        # the main command
        mode = self.label_mode["text"]

        if mode == "Mode":  # if not clicked any button
            self.message_show_result["text"] = "Please select a command first !"
            return

        elif self.lineEdit.get() == "":  # if LineEdit is empty
            self.message_show_result["text"] = "Please write your command in entry !"
            return

        # else and having no problems:
        elif mode == "NEAREST-PEND-ORDER":
            mode = "GET-NEAREST-PENDING-ORDER"

        try:
            text = " ".join([i for i in self.lineEdit.get().split(" ") if " " not in i and i])
            self.message_show_result["text"] = self.command.main(True, [mode + " " + text])

        except Exception:
            self.message_show_result["text"] = "Wrong entrance !"


if __name__ == '__main__':
    # run program by calling main of Command not graphical
    command = Command()
    command.main()

    # GUI
    # roots = tk.Tk()
    # roots.title("Application GUI")
    #
    # widths, heights = 600, 500
    # screenwidth, screenheight = roots.winfo_screenwidth(), roots.winfo_screenheight()
    # align_str = '%dx%d+%d+%d' % (widths, heights, (screenwidth - widths) / 2, (screenheight - heights) / 2)
    # roots.geometry(align_str)
    # roots.resizable(width=False, height=False)
    # roots.configure(background='#569FE7')
    #
    # app = GraphicalMenu(root=roots)
    # roots.mainloop()
