"""
Name
    Mainframe

DESCRIPTION
    This module contains the class allowing the user to add/delete/update/select items for a selected
    car in the maintenance list

CLASS
    Main Frame            -- object to store methods for allowing user to perform car maintenance

FUNCTION
    __init__              -- stores master, and tk in the MainFrame window
                             object, and initializes the widgets in the window
                             allowing the user to perform car maintenance
    do_backup             -- backup the maintenance data
    do_restore            -- restore the maintenance data
    set_option_background -- set the background color to highlight user selecting DELETE option
    build_car_list        -- stores the car name for the selected car in the scroll list visible to the
                             user to allow for car selection
    display_items         -- clears the MainFrame view and activates the ItemsFrame view
    display_add_car       -- clears the MainFrame view and activates the AddCarFrame view
    display_info          -- clears the MainFrame view and activates the MaintInfoFrame view
    on_car_select         -- performs the following based on option menu selection:
                             Display Maintenance Items option - activates PerformMaintFrame view
                             Delete Selected Car option - delete item from car's maintenance list

DATA
    self                  -- contains the Frame object used for viewing
    self.master           -- contains the calling class to allow calling its methods
    self.tk               -- contains tkinter to allow creating window elements
                             (Labels, Buttons, Entries)
    cm.car_data           -- contains the CarMaintenance data object
    cm.selections         -- contains the user selected car name and item name
"""

import carmaintenance as cm
from tkinter import *
from PIL import ImageTk, Image


#
# Provide data/methods for the MainFrame window
#
class MainFrame(Frame):

    # initialize the window contents and store data in object
    def __init__(self, master, tk):
        super(Frame).__init__()
        self.master = master
        self.tk = tk

        self.frame = Frame(self.tk, bg=self.tk.background)
        self.frame.pack(fill=BOTH, expand=TRUE)

        # Create and insert phone background image
        load_file = "phone-background.png"
        img = Image.open(load_file)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        load_file = "phone-hdr.png"
        img = Image.open(load_file)
        photo = ImageTk.PhotoImage(img)
        self.img_hdr_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_hdr_panel.image = photo
        self.img_hdr_panel.place(x=20, y=80, anchor=NW)

        # Create exit button to exit the car maintenance data
        self.exit_button = Button(self.frame, text="Exit", command=self.master.do_exit, bd=0, font=('Helvetica', 10))
        self.exit_button.config(borderwidth=1, bg=self.tk.background)
        self.exit_button.place(x=10, y=100, anchor=NW)

        # Create backup button to backup the car maintenance data
        self.backup_button = Button(self.frame, text="Backup", command=self.do_backup, bd=0, font=("Helvetica", 10))
        self.backup_button.config(borderwidth=1, bg=self.tk.background)
        self.backup_button.place(x=160, y=100, anchor=NW)
        # self.backup_button.config(state=DISABLED)

        # Restore the previously backed up car mainenance data
        self.restore_button = Button(self.frame, text="Restore", command=self.do_restore, bd=0, font=("Helvetica", 10))
        self.restore_button.config(borderwidth=1, bg=self.tk.background)
        self.restore_button.place(x=220, y=100, anchor=NW)

        # Create and insert car image
        load_file = "car.png"
        img = Image.open(load_file)
        img = img.resize((30,30),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=120, y=160, anchor=CENTER)

        # Create label to indicate the list of cars stored
        self.car_name_label = Label(self.frame, text="Cars", font=("Helvetica", 18), bg=self.tk.background)
        self.car_name_label.place(x=170, y=160, anchor=CENTER)
        self.car_device_label = Label(self.frame, text="on my device", font=("Helvetica", 10), bg=self.tk.background)
        self.car_device_label.place(x=150, y=190, anchor=CENTER)

        # Create list box to show all the cars stored
        self.scrollbar = Scrollbar(self.frame, orient="vertical")
        self.list_nodes = Listbox(self.frame, exportselection=0, yscrollcommand=self.scrollbar.set,
                                  font=("Helvetica", 12))
        self.list_nodes.place(x=10, y=220, anchor=NW)
        self.list_nodes.config(width=29)
        self.list_nodes.bind("<<ListboxSelect>>", self.on_car_select)
        self.scrollbar.place(x=270, y=140, height=200, anchor=NW)
        self.scrollbar.config(command=self.list_nodes.yview)

        # Create label and drop down menu to select between displaying maintenance info or deleting cars in list box
        self.selection_mode_label = Label(self.frame, text="Selection Mode:", font=("Helvetica", 10), bg=self.tk.background)
        self.selection_mode_label.place(x=55, y=450, anchor=CENTER)
        self.dropOptions=["Display Maintenance Items", "Delete Selected Car"]
        self.dropVar = StringVar()
        self.dropVar.set(self.dropOptions[0])  # default choice
        self.selection_mode_button = OptionMenu(self.frame, self.dropVar, *self.dropOptions,
                                                command=self.set_option_background)
        self.selection_mode_button.config(bg=self.tk.background)
        self.selection_mode_button.place(x=195, y=450, anchor=CENTER)
        self.original_option_background_color = self.selection_mode_button.cget("background")

        # create add button to add cars to the maintenance list
        self.add_car_button = Button(self.frame, text="Add Car", command=self.display_add_car,
                                    font=("Helvetica", 10), bg=self.tk.background)
        self.add_car_button.config(borderwidth=2, width=8)
        self.add_car_button.place(x=15, y=530, anchor=SW)

        # create info button to view current maintenance needs
        self.info_button = Button(self.frame, text="View All", command=self.display_info,
                                  font=("Helvetica", 10), bg=self.tk.background)
        self.info_button.config(borderwidth=2, width=8)
        self.info_button.place(x=285, y=530, anchor=SE)

        # inserts the car names into the ListBox
        self.build_car_list()

    # backup the car data
    def do_backup(self):
        try:
            cm.store_car_maintenance_data(cm.car_data, cm.backup_and_restore_file_name)
        except OSError:
            print("Error backing up file to "+cm.backup_and_restore_file_name)
        else:
            self.master.activate_main_window()

    # restore the car data from backup file
    def do_restore(self):
        try:
            cm.car_data = cm.retrieve_car_maintenance_data(cm.backup_and_restore_file_name)
        except OSError:
            print("Error restoring from backup file "+cm.backup_and_restore_file_name)
        else:
            self.master.activate_main_window()

    # Highlight the background color if delete mode selected
    def set_option_background(self, value):

        # set background color to yellow if in delete mode
        if value == self.dropOptions[1]:
            self.selection_mode_button.config(background='yellow')
            self.info_button.config(text="Delete", background='yellow')
        else:
            self.selection_mode_button.config(background=self.original_option_background_color)
            self.info_button.config(text="View All", background=self.original_option_background_color)

    # stores the car names for the selected cars in the visible scroll list
    def build_car_list(self):
        self.list_nodes.delete(0, self.list_nodes.size())
        car_list = cm.car_data.get_car_list()
        car_index=0
        if car_list is not None:
            for car in car_list:
                car_text_entry = car.replace('_', ' ')
                self.list_nodes.insert(END, car_text_entry)

                # set the background color to yellow if the car has items needed maintenance
                if cm.car_data.does_car_need_maintenance(car):
                    self.list_nodes.itemconfig(car_index, {'bg': 'yellow'})
                else:
                    self.list_nodes.itemconfig(car_index, {'bg': 'white'})
                car_index = car_index+1

    # activates the ItemsFrame view
    def display_items(self):
        self.master.activate_items_window()

    # activates the AddCarFrame view
    def display_add_car(self):
        self.master.activate_add_car_window()

    # activates the MaintInfo view
    def display_info(self):
        self.master.activate_maint_info_window()

    # Display Maintenance Items option selected - selection activates the ItemsFrame view
    # Delete Selected Car option selected - selection deletes the selected car from the maintenance list
    def on_car_select(self, event=None):

        curselection = self.list_nodes.curselection()

        # verify actual car selected
        if curselection:
            car_text_entry = self.list_nodes.get(curselection[0])
            car = car_text_entry.replace(' ', '_')
            cm.selections.set_car_selected(car)

            # if in display mode cactivate the ItemsFrame view
            if self.dropVar.get() == "Display Maintenance Items":
                self.master.activate_items_window()

            # else in delete mode - delete the car from the list, reactivate MainFrame view
            else:
                car = cm.selections.get_car_selected()
                cm.car_data.del_car(car)
                cm.selections.set_car_selected("")

                # reset the mode back to display mode to prevent accidental deletes
                self.dropVar.set(self.dropOptions[0])
                self.selection_mode_button.config(background=self.original_option_background_color)
                self.master.activate_main_window()

