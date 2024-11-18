# Project 1 (TPRG2131) test_Vending_machine.py
# Student Name- Gurleen Kaur Jassal 
# Student ID- 100942372
# Due Date- 17 November 2024
# Instructor - Philip J
# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s).

"""
For the 'vending_machine_graphical.py' script - WORKS
"""

import pytest
from vending_machine_GKJ import VendingMachine, WaitingState, AddCoinsState, DeliverProductState, CountChangeState


def test_vendingMachine():
    # new machine object
     vending = VendingMachine()   
# Add the states - ORG
#vending.add_state(WaitingState())
#vending.add_state(coinsState())
#vending.add_state(Dispensestate())
#vending.add_state(ChangeState())
      # My revisions
     vending.add_state(WaitingState())
     vending.add_state(AddCoinsState())
     vending.add_state(DeliverProductState())
     vending.add_state(CountChangeState())
     
      # Reset state is "waiting for first coin"
     vending.go_to_state('waiting')
     assert vending.state.name == 'waiting'    # Verify the current state is 'waiting'

 # test that the first coin causes a transition to 'coins'
     vending.event = '200' # Simulate inserting a 200 coin
     vending.update()   # Update the vending machine state
     assert vending.state.name == 'add_coins'     # Verify the state is now 'add_coins'
     assert vending.amount == 200 # Check the total amount is 200
     
     vending.event = '100' # Simulate inserting a 100 coin
     vending.update()  # Update the vending machine state
     assert vending.state.name == 'add_coins' # Verify the state remains 'add_coins'
     assert vending.amount == 300  # Check the total amount is now 300
     
     vending.event = '25'   # Simulate inserting a 25 coin
     vending.update() # Update the vending machine state
     assert vending.state.name == 'add_coins'  # Verify the state remains 'add_coins'
     assert vending.amount == 325 # Check the total amount is now 325


     vending.event = '10'  # Simulate inserting a 10 coin
     vending.update()  # Update the vending machine state
     assert vending.state.name == 'add_coins' # Verify the state remains 'add_coins'
     assert vending.amount == 335 # Check the total amount is now 335

     
     vending.event = '5'  # Simulate inserting a 5 coin
     vending.update() # Update the vending machine state
     assert vending.state.name == 'add_coins' # Verify the state remains 'add_coins'
     assert vending.amount == 340  # Check the total amount is now 340
