import sqlite3


# Database Declaration
db = sqlite3.connect('C:/Users/ethan/Desktop/Databases/assessment.db')
cursor = db.cursor()
# Database Declaration


# Functions
def get_shopper_id():
    shopper_id_found = True
    while shopper_id_found:
        shopperIDList = [row[0] for row in db.execute(idFindQuery)]
        shopper_id = input('Enter Valid Shopper ID: ')
        if shopper_id in shopperIDList:
            print(get_menu_choice())
        else:
            print('Cannot find shopper ID, proceeding to exit...')

def get_menu_choice():
    loop = True
    while loop:
        get_menu_items(menu_options, title)
        
        choice = input("Enter your choice [1-5]: ")
        if choice == 1:
            loop = True
        elif choice == 2:
            loop = True
        elif choice == 3:
            loop = True
        elif choice == 4:
            loop = True
        elif choice == 5:
            loop = False
        else:
            print 'Wrong menu selection, enter any key to try again...\n\n'
    return [choice]

def get_menu_items(menu_options, title):
        print(title)
        print(73 * "-")
        for option in menu_options:
            print option[0]
# Functions


# Main Display Menu
title = 'ORINOCO - SHOPPER MAIN MENU'
menu_options = [
    ['1) Display your order history','Hi'],
    ['2) Add an item to your basket','Hi'],
    ['3) View your basket','Hi'],
    ['4) Checkout','Hi'],
    ['5) Exit','Hi']]
# Main Display Menu


# Queries
idFindQuery = 'SELECT shopper_id FROM shoppers'

# Queries



print(get_shopper_id())