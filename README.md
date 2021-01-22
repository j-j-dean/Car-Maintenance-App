# Car Maintenance App
This application was designed to help identify if my car needed maintenance just by updating the car's 
current mileage.  I originally wrote it to run on my iPhone using an app from the app store called 
Pythonista.  Pythonista can run python scripts and provides a user interface compatible for iPhone.

## About this application
This version of the program was written in Python version 3.6 to run on Windows.  Cars can be added
or deleted with this application as needed.  Items requiring maintenance for each car can also be
added or deleted as needed.  By simply changing the current mileage as needed for each car the 
application will highlight any cars requiring maintenance.  And a convenient viewing from the main
screen will identify all maintenance that is currently needed.

# carmaintmain.py
This file starts the process by creating and loading the user interface.

# carmaintenance.py
This file contains the classes and the objects that store all the maintenance data including: 
a list of cars being maintained, a list of items for each car being maintained, and
the current user selections being traversed while examining a car's maintenance history.
