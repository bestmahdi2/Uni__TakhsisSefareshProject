from Tools import ServiceCategory, OrderStatus, Tools


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
