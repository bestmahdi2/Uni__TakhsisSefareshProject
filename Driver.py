from Tools import ServiceCategory, DriverStatus, Tools


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
