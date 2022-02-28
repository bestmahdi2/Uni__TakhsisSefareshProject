import tkinter as tk
import tkinter.font as tk_font
from functools import partial

from Command import Command


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


if __name__ == "__main__":
    roots = tk.Tk()
    roots.title("Application GUI")

    widths, heights = 600, 500
    screenwidth, screenheight = roots.winfo_screenwidth(), roots.winfo_screenheight()
    align_str = '%dx%d+%d+%d' % (widths, heights, (screenwidth - widths) / 2, (screenheight - heights) / 2)
    roots.geometry(align_str)
    roots.resizable(width=False, height=False)
    roots.configure(background='#569FE7')

    app = GraphicalMenu(root=roots)
    roots.mainloop()
