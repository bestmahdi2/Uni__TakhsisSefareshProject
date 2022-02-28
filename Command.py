from Order import Order
from Driver import Driver
from Tools import OrderStatus, DriverStatus, Tools, ServiceCategory


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


if __name__ == '__main__':
    # run program by calling main of Command
    command = Command()
    command.main()
