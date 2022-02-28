import enum
import re
from typing import Union, Tuple


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
