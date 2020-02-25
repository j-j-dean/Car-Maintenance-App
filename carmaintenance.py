"""
Name
    carmaintenance

DESCRIPTION
    This module contains the classes for storing and performing operations
    for a list of cars to maintain and the items for each car.

CLASS
    UserSelections -- object to store the current car and item selected by the user
    MaintenanceItem-- object to store frequency of maintenance in miles and months, and the
                      mileage and date when maintenance was last performed
    CarToMaintain  -- object to store the car name and mileage and the MaintenanceItem 
                      objects associated with the car
    CarMaintenance -- contains the CarToMaintain objects for all cars being maintainted
                      and methods for accessing and modifying those objects

FUNCTION
                            -- UserSelection methods
    set_car_selected                 -- Getters and Setters
    get_car_selected
    set_item_selected
    get_item_selected
                            -- CarToMaintain methods
    add_maintenance_item                 -- Add MaintainItem object for selected car
    del_maintenance_item                 -- Delete MaintainItem object for selected car
    get_maintenance_item_freq_miles      -- Getters and Setters
    get_maintenance_item_freq_time
    get_maintenance_item_last_mileage
    get_maintenance_item_last_date
                           -- CarMaintenance methods
    add_car                           -- Add CarToMaintain object corresponding to
                                         newly selected car name
    del_car                           -- Delete CarToMaintain object for selected car
    is_new_car                        -- Check to see if car name specified is new
                                         or a duplicate in list of cars
    does_car_need_maintenance         -- Check to see if selected car needs maintenance
    is_new_item                       -- Check to see if item specified is new or a
                                         duplicate item for the selected car
    does_item_need_maintenance        -- Check to see if selected car needs maintenance
    add_car_items                     -- Add MaintenanceItem object for selected car
    del_car_items                     -- Delete MaintenanceItem object for selected car
    get_car_list                      -- Getter to return list of all cars
    get_items_list                    -- Getter to return list of items for specified car
    get_mileage                       -- Getters and Setters (CarMaintenance methods)
    get_item_freq_miles
    get_item_freq_time
    get_item_last_mileage
    get_item_last_date
    set_mileage
                           -- Additional Functions
    add_months_to_date                -- returns a new date by adding a specified number of months to a
                                         specified date
    store_car_maint_data              -- store the data to disc
    retrieve_car_maint_data           -- retrieve the data from disc

DATA
    selections                     -- stores the car and item selected by the user
    filename                       -- used to store and retieve car maintenance data
    car_data                       -- contains the CarMaintenance data object
    
"""

import pickle
from datetime import datetime

# filename is the file and directory where the maintenance data will be stored
storage_file_name = 'CarMaintenance.dat'
backup_and_restore_file_name = 'CarMaintenance.bak'

# object to store the current car and item selected by the user
class UserSelections:

    # store data in object
    def __init__(self):
        self.carSelected = ""
        self.itemSelected = ""

    # setter - sets carSelected
    def set_car_selected(self, car):
        self.carSelected = car

    # getter - returns carSelected
    def get_car_selected(self):
        return self.carSelected

    # setter - sets itemSelected
    def set_item_selected(self, itemSelected):
        self.itemSelected = itemSelected

    # getter - gets itemSelected
    def get_item_selected(self):
        return self.itemSelected


"""MaintenanceItem object stores the inital mileage and date, the frequency 
   of maintenance in miles and time(months), the mileage and date for the
   last time this maintenance was performed"""
class MaintenanceItem:

    # initializes the object contents
    def __init__ (self, freq_miles, freq_time, last_mileage, last_date):
        self.freq_miles = freq_miles
        self.freq_time = freq_time
        self.last_mileage = last_mileage
        self.last_date = last_date

    # provides method for printing object to standard out
    def __repr__ (self):
        return_string = str(self.freq_miles) + ' ' + str(self.freq_time) + ' ' + \
                        str(self.last_mileage) + ' ' + str(self.last_date)
        return return_string


# CarToMaintain object stores the maintenance item objects associated with a car
class CarToMaintain:

    # initialize the car description and mileage when object created
    def __init__(self, car_name, mileage):
        self.car_name = car_name
        self.mileage = mileage
        self.items = {}

    # method for iterating over the maintenance items
    def __iter__ (self):
        for item in self.items:
            yield item

    # method for printing object to standard out
    def __repr__(self):
        if self.items == {}:
            return "No maintenance items listed"
        else:
            return str(self.items)

    # method for a new maintenance item object
    def add_maintenance_item(self,item_name, freq_miles, freq_time, last_mileage, last_date):
        new_item = MaintenanceItem(freq_miles, freq_time, last_mileage, last_date)
        self.items[item_name] = new_item

    # method for deleting a maintenance item object
    def del_maintenance_item(self, item_name):
        del self.items[item_name]

    # Getters
    def get_maintenance_item_freq_miles(self, item_name):
        return self.items[item_name].freq_miles

    def get_maintenance_item_freq_time(self, item_name):
        return self.items[item_name].freq_time

    def get_maintenance_item_last_mileage(self, item_name):
        return self.items[item_name].last_mileage

    def get_maintenance_item_last_date(self, item_name):
        return self.items[item_name].last_date

# Car Maintenance object stores the cars and the list of items for each car being maintained
class CarMaintenance:

    # initialize the cars dictionary
    def __init__(self):
        self.cars = {}

    # method to iterate over the cars dictionary
    def __iter__(self):
        for car in self.cars:
            yield car

    # method to print cars list to standard out
    def __repr__(self):
        if self.cars == {}:
            return "No cars listed!"
        else:
            return str(self.cars)

    # method to add a new car to maintenance object
    def add_car(self, car_name, mileage):
        new_car = CarToMaintain(car_name, mileage)
        self.cars[car_name] = new_car

    # method to delete a selected car
    def del_car(self, car_name):
        del self.cars[car_name]
    
    # method to verify car is an original and not a duplicate entry
    def is_new_car(self, car_name):
        if car_name == "" or self.cars.get(car_name):
            return False  # Not a new car - already exists
        else:
            return True  # Yes it is a new car

    # method to determine if car needs maintenance
    def does_car_need_maintenance(self, car_name):
        need = False
        item_list = self.get_items_list(car_name)
        for item in item_list:
            if self.does_item_need_maintenance(car_name, item):
                need = True
        return need

    # method to verify item is an original and not a duplicate entry
    def is_new_item(self, car_name, item_name):
        if item_name == "" or self.cars[car_name].items.get(item_name):
            return False  # Not a new item - already exists
        else:
            return True  # Yes it is a new item

    # method to determine if item needs maintenance for selected car
    def does_item_need_maintenance(self, car_name, item_name):
        need = False
        mileage = self.get_mileage(car_name)
        item_last_mileage = self.get_item_last_mileage(car_name, item_name)
        item_freq_miles = self.get_item_freq_miles(car_name, item_name)
        if mileage == "": mileage = "0"
        if item_last_mileage == "": item_last_mileage = "0"
        if item_freq_miles == "": item_freq_miles = "0"

        # check based on mileage
        if item_last_mileage == "0":
            if item_freq_miles != "0" and int(mileage) > int(item_freq_miles):
                need = True
        elif  item_freq_miles != "0":
            change_mileage = int(item_last_mileage) + int(item_freq_miles)
            if int(mileage) > change_mileage:
                need = True

        # check based on date
        time_freq = self.get_item_freq_time(car_name, item_name)
        item_last_date = self.get_item_last_date(car_name, item_name)
        date = datetime.now()
        if item_last_date != "" and time_freq != "":
            item_last_datetime = datetime.strptime(item_last_date, '%m/%d/%Y')
            change_date = add_months_to_date(item_last_datetime, int(time_freq))
            if date > change_date:
                 need = True

        return need

    # method to add maintenance item for a selected car
    def add_car_items(self, car_name, item_name, freq_miles, freq_time, last_mileage, last_date):
        self.cars[car_name].add_maintenance_item(item_name, freq_miles, freq_time, last_mileage, last_date)

    # method to delete maintenance item for a selected car
    def del_car_items(self, car_name, item_name):
        self.cars[car_name].del_maintenance_item(item_name)

    # method to return a list of all the cars being maintained
    def get_car_list(self):
        car_list = []
        for car in self.cars:
            car_list.append(car)
        return car_list

    # method to return a list of items being maintained for the selected car
    def get_items_list(self, car):
        items_list = []
        if car:
            for item in self.cars[car]:
                items_list.append(item)
        return items_list

    # Getters
    def get_mileage(self, car_name):
        return self.cars[car_name].mileage

    def get_item_freq_miles(self, car_name, item_name):
        return self.cars[car_name].get_maintenance_item_freq_miles(item_name)

    def get_item_freq_time(self, car_name, item_name):
        return self.cars[car_name].get_maintenance_item_freq_time(item_name)

    def get_item_last_mileage(self, car_name, item_name):
        return self.cars[car_name].get_maintenance_item_last_mileage(item_name)

    def get_item_last_date(self, car_name, item_name):
        return self.cars[car_name].get_maintenance_item_last_date(item_name)

    # Setters
    def set_mileage(self, car_name, mileage):
        self.cars[car_name].mileage = mileage

# function that returns a new date after adding a specified number of months to a specified date
def add_months_to_date(date, num_months):
    import datetime
    one_day = datetime.timedelta(days=1)
    current_day = date.day
    one_month_later = date
    current_month = date.month
    while num_months > 0:
        num_months -= 1
        one_month_later += one_day
        while one_month_later.month == current_month:
            one_month_later += one_day
        current_month = one_month_later.month
        while one_month_later.day < current_day:
            one_month_later += one_day
            if one_month_later.month != current_month:
                one_month_later -= one_day
                break
    return one_month_later

# stores car maintenance data to disc
def store_car_maintenance_data(car_data, file_name):
    try:
        file = open(file_name, 'wb')
    except OSError:
        print("Error opening file "+file_name)
        print("Unable to store data to file")
    else:
        pickle.dump(car_data, file)
        file.close()


# retrieves car maintenance data from disc
def retrieve_car_maintenance_data(file_name):
    stored_car_data = CarMaintenance()
    try:
        file = open(file_name, 'rb')
    except OSError:
        print("Error opening file " + file_name)
        print("Unable to retrieve data from file (file may not exist yet)")
    else:
        stored_car_data = pickle.load(file)
        file.close()

    return stored_car_data

#
# Create object to store the user's selections
#
selections = UserSelections()

#
# Retrieve the stored car maintenance data
#
car_data = retrieve_car_maintenance_data(storage_file_name)