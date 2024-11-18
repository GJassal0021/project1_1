# Project 1 (TPRG2131) Vending_machine.py
# Student Name- Gurleen Kaur Jassal
# Student ID- 100942372
# Due Date- 17 November 2024
# Instructor - Philip J
# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

#!/usr/bin/env python3

# STUDENT version for Project 1.
# TPRG2131 Fall 2024
# Updated Phil J (Fall 2024)
#
# Louis Bertrand
# Oct 4, 2021 - initial version
# Nov 17, 2022 - Updated for Fall 2024.
#

# PySimpleGUI recipes used:
#
# Persistent GUI example
# https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-pattern-2a-persistent-window-multiple-reads-using-an-event-loop
#
# Asynchronous Window With Periodic Update
# https://pysimplegui.readthedocs.io/en/latest/cookbook/#asynchronous-window-with-periodic-update

import PySimpleGUI as sg  # Importing the PySimpleGUI library for GUI creation
import time  # Importing time module for delays

# Hardware interface module
# Button basic recipe: *** define the pin you used
# https://gpiozero.readthedocs.io/en/stable/recipes.html#button
# Button on GPIO channel, BCM numbering, same name as Pi400 IO pin
# Hardware interface module

hardware_present = False  # Flag to check if hardware is present
try:
    from gpiozero import Button, Servo  # Importing Button and Servo from gpiozero
    servo = Servo(17)  # Initializing Servo on GPIO pin 17
    key1 = Button(5)  # Initializing Button on GPIO pin 5
    hardware_present = True  # Setting flag to True if hardware is present
except ModuleNotFoundError:
    print("Not on a Raspberry Pi or gpiozero not installed.")  # Error message if hardware is not present

# Setting this constant to True enables the logging function
# Set it to False for normal operation
TESTING = True  # Flag for enabling/disabling logging

# Print a debug log string if TESTING is True, ensure use of Docstring, in definition
def log(s):  # Log function definition
    if TESTING:  # Check if testing is enabled
        print(s)  # Print log message

# The vending state machine class holds the states and any information
# that "belongs to" the state machine. In this case, the information
# is the products and prices, and the coins inserted and change due.
# For testing purposes, output is to stdout, also ensure use of Docstring, in class
class VendingMachine(object):  # VendingMachine class definition
    PRODUCTS = {  # Dictionary of products and their prices
        "suprise": ("SURPRISE", 5),
        "chocolate": ("CHOCOLATE", 10),
        "soda": ("SODA", 15),
        "chips": ("CHIPS", 20),
        "candy": ("CANDY", 25)
    }

    COINS = {  # Dictionary of coin values
        "5": ("NICKEL", 5),
        "10": ("DIME", 10),
        "25": ("QUARTER", 25),
        "100": ("LOONIE", 100),
        "200": ("TOONIE", 200)
    }

    def __init__(self):  # Constructor for VendingMachine
        self.state = None  # Current state of the machine
        self.states = {}  # Dictionary to hold states
        self.event = ""  # Current event
        self.amount = 0  # Amount of money inserted
        self.change_due = 0  # Change to be returned
        self.coin_values = sorted([self.COINS[k][1] for k in self.COINS], reverse=True)  # Sorted coin values
        log(str(self.coin_values))  # Log coin values

    def add_state(self, state):  # Method to add a state
        self.states[state.name] = state  # Add state to the dictionary

    def go_to_state(self, state_name):  # Method to transition to a new state
        if self.state:  # If there is a current state
            log(f'Exiting {self.state.name}')  # Log exiting state
            self.state.on_exit(self)  # Call on_exit method of current state
        self.state = self.states[state_name]  # Set new state
        log(f'Entering {self.state.name}')  # Log entering new state
        self.state.on_entry(self)  # Call on_entry method of new state

    def update(self):  # Method to update the current state
        if self.state:  # If there is a current state
            self.state.update(self)  # Call update method of current state

    def add_coin(self, coin):  # Method to add a coin
        self.amount += self.COINS[coin][1]  # Increase amount by coin value

    def button_action(self):  # Method to handle button action
        self.event = 'RETURN'  # Set event to RETURN
        self.update()  # Update the state machine

# Parent class for the derived state classes
# It does nothing. The derived classes are where the work is done.
# However this is needed. In formal terms, this is an "abstract" class.
class State(object):  # State class definition
    _NAME = ""  # Placeholder for state name
    
    @property
    def name(self):  # Property to get state name
        return self._NAME  # Return state name
    
    def on_entry(self, machine):  # Method called on entering state
        pass  # No action on entry
    
    def on_exit(self, machine):  # Method called on exiting state
        pass  # No action on exit
    
    def update(self, machine):  # Method to update state
        pass  # No action on update

# In the waiting state, the machine waits for the first coin
class WaitingState(State):  # WaitingState class definition
    _NAME = "waiting"  # State name
    
    def update(self, machine):  # Update method for waiting state
        if machine.event in machine.COINS:  # If event is a coin
            machine.add_coin(machine.event)  # Add coin to amount
            machine.go_to_state('add_coins')  # Transition to add_coins state

class AddCoinsState(State):  # AddCoinsState class definition
    _NAME = "add_coins"  # State name
    
    def update(self, machine):  # Update method for add_coins state
        if machine.event == "RETURN":  # If event is RETURN
            machine.change_due = machine.amount  # Set change due
            machine.amount = 0  # Reset amount
            machine.go_to_state('count_change')  # Transition to count_change state
        elif machine.event in machine.COINS:  # If event is a coin
            machine.add_coin(machine.event)  # Add coin to amount
        elif machine.event in machine.PRODUCTS:  # If event is a product
            if machine.amount >= machine.PRODUCTS[machine.event][1]:  # Check if enough money
                machine.go_to_state('deliver_product')  # Transition to deliver_product state

class DeliverProductState(State):  # DeliverProductState class definition
    _NAME = "deliver_product"  # State name
    
    def on_entry(self, machine):  # Method called on entering deliver_product state
        machine.change_due = machine.amount - machine.PRODUCTS[machine.event][1]  # Calculate change due
        machine.amount = 0  # Reset amount
        if hardware_present:  # If hardware is present
            print(f"Delivering {machine.PRODUCTS[machine.event][0]}")  # Deliver product
            self.move_servo()  # Move servo to deliver product
        else:  # If hardware is not present
            print(f"Buzz... Whir... Click... {machine.PRODUCTS[machine.event][0]}")  # Simulate delivery
        if machine.change_due > 0:  # If change is due
            machine.go_to_state('count_change')  # Transition to count_change state
        else:  # If no change is due
            machine.go_to_state('waiting')  # Transition to waiting state

    def move_servo(self):  # Method to move servo
        servo.min()  # Move servo to minimum position
        time.sleep(0.5)  # Wait for half a second
        servo.mid()  # Move servo to middle position
        time.sleep(0.5)  # Wait for half a second
        servo.max()  # Move servo to maximum position
        time.sleep(0.5)  # Wait for half a second
        servo.mid()  # Move servo back to middle position

class CountChangeState(State):  # CountChangeState class definition
    _NAME = "count_change"  # State name
    
    def on_entry(self, machine):  # Method called on entering count_change state
        print(f"Change due: ${machine.change_due / 100:.2f}")  # Print change due
        log(f"Returning change: {machine.change_due}")  # Log change due
    
    def update(self, machine):  # Update method for count_change state
        for coin_value in machine.coin_values:  # Iterate through coin values
            while machine.change_due >= coin_value:  # While change due is greater than or equal to coin value
                print(f"Returning {coin_value}")  # Print returning coin
                machine.change_due -= coin_value  # Decrease change due by coin value
        if machine.change_due == 0:  # If no change is due
            machine.go_to_state('waiting')  # Transition to waiting state

if __name__ == "__main__":  # Main program execution
    sg.theme('BluePurple')  # Set theme for the GUI

    coin_col = [[sg.Text("ENTER COINS", font=("Helvetica", 24))]]  # Column for coin entry
    coin_col.extend([[sg.Button(item, font=("Helvetica", 18))] for item in VendingMachine.COINS])  # Add coin buttons

    select_col = [[sg.Text("SELECT ITEM", font=("Helvetica", 24))]]  # Column for item selection
    select_col.extend([[sg.Button(item, font=("Helvetica", 18))] for item in VendingMachine.PRODUCTS])  # Add product buttons

    layout = [  # Layout for the GUI
        [sg.Column(coin_col, vertical_alignment="TOP"),  # Coin column
         sg.VSeparator(),  # Vertical separator
         sg.Column(select_col, vertical_alignment="TOP")],  # Product column
        [sg.Button("RETURN", font=("Helvetica", 12))]  # Return button
    ]
    window = sg.Window('Vending Machine', layout)  # Create the window

    vending = VendingMachine()  # Initialize VendingMachine
    vending.add_state(WaitingState())  # Add waiting state
    vending.add_state(AddCoinsState())  # Add add_coins state
    vending.add_state(DeliverProductState())  # Add deliver_product state
    vending.add_state(CountChangeState())  # Add count_change state
    vending.go_to_state('waiting')  # Transition to waiting state

    if hardware_present:  # If hardware is present
        key1.when_pressed = vending.button_action  # Set button action

    # The Event Loop: begin continuous processing of events
    # The window.read() function reads events and values from the GUI.
    # The machine.event variable stores the event so that the
    # update function can process it.
    # Now that all the states have been defined this is the
    # main portion of the main program.
    while True:  # Infinite loop for event processing
        event, values = window.read(timeout=10)  # Read events from the window
        if event != '__TIMEOUT__':  # If event is not a timeout
            log((event, values))  # Log the event and values
        if event in (sg.WIN_CLOSED, 'Exit'):  # If window is closed or exit button is pressed
            break  # Exit the loop
        vending.event = event  # Set the event in the vending machine
        vending.update()  # Update the vending machine

    window.close()  # Close the window
    print("Normal exit")  # Print exit message
