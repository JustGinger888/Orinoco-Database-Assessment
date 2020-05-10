import sqlite3


# Database Declaration
db = sqlite3.connect('C:/Users/ethan/Desktop/Databases/assessment.db')
cursor = db.cursor()
# Database Declaration


# Functions
## Initial Input Of Shopper ID To Get Corresponding DB Data
def get_shopper_id(shopper_id):
    # Initiate Loop
    shopper_id_found = True
    while shopper_id_found:
        # Add List of valid Shopper IDs from DB
        shopperIDList = [row[0] for row in db.execute(idFindQuery)]
        
        # If Found
        if shopper_id in shopperIDList:
            print(get_menu_choice(shopper_id))
            shopper_id_found = False
        # Not Found
        else:
            print('Cannot find shopper ID, proceeding to exit...')
            shopper_id_found = False
    return ''

## Gets, Displays and Compares the Menu Choices
def get_menu_choice(shopper_id):
    loop = True
    while loop:
        # Display Menu Options
        get_menu_items(menu_options, title)
        
        # Check Menu Items
        choice = input('Enter your choice [1-5]: ')
        if choice == 1:
            menu_choice_01(shopper_id)
        elif choice == 2:
            menu_choice_02(shopper_id)
        elif choice == 3:
            menu_choice_03(shopper_id)
        elif choice == 4:
            menu_choice_04()
        elif choice == 5:
            menu_choice_05()
            loop = False
        else:
            menu_choice_05()
    return ''

## Displays Title And Layout Of Choices
def get_menu_items(menu_options, title):
        print(title)
        print(73 * "-")
        for option in menu_options:
            print option[0]

#Menu Choices
def menu_choice_01(shopper_id):
    #Get SQL Query for option 1
    cursor.execute(menu_options[0][1])
    myResult = cursor.fetchall()

    if myResult != None:
        for x in myResult:
            print(x)
        print('\n\n')
    else:
        print 'No orders placed by this customer'

def menu_choice_02(shopper_id):
    #Get SQL Query for option 2
    cursor.execute(menu_options[1][1])
    myResult = cursor.fetchall()
    if myResult != None:
        for x in myResult:
            print(x)
        print('\n\n')
    else:
        print 'Error'

def menu_choice_03(shopper_id):
    #Get SQL Query for option 3
    cursor.execute(menu_options[2][1])
    myResult = cursor.fetchall()

    if myResult != None:
        for x in myResult:
            print(x)
        print('\n\n')
    else:
        print 'Error'

# Option 4 Not Implimented
def menu_choice_04():
    print('Not implemented')

# Exit Program
def menu_choice_05():
    print('Exiting\n\n')
    db.close()
#MenuChoices
# Functions


#Prompting Input Of Shoope ID
shopper_id = input('Enter Valid Shopper ID: ')


# Main Display Menu
title = 'ORINOCO - SHOPPER MAIN MENU'
menu_options = [
    ['1) Display your order history', queryOption01],
    ['2) Add an item to your basket', queryOption02],
    ['3) View your basket', queryOption03],
    ['4) Checkout','N/A'],
    ['5) Exit','N/A']]
# Main Display Menu


# Queries
idFindQuery = 'SELECT shopper_id FROM shoppers'
queryOption01 = ('SELECT shopper_orders.order_id, '+
                 'shopper_orders.order_date, '+ 
                 'products. product_description, '+
                 'sellers.seller_name, '+
                 'ordered_products.price, '+
                 'ordered_products.quantity, '+
                 'ordered_products.ordered_product_status as Status '+
                 'FROM shoppers '+
                 'INNER JOIN shopper_orders ON shoppers.shopper_id = shopper_orders.shopper_id '+
                 'INNER JOIN ordered_products ON shopper_orders.order_id = ordered_products.order_id '+
                 'INNER JOIN products ON ordered_products.product_id = products.product_id  '+
                 'INNER JOIN sellers ON ordered_products.seller_id = sellers.seller_id  '+
                 'WHERE shoppers.shopper_id = % s ORDER BY shopper_orders.order_date DESC'% shopper_id)

queryOption02 = ''

queryOption03 = ('SELECT product_description, '+
                 'sellers.seller_name, '+ 
                 'basket_contents.quantity, '+
                 'basket_contents.price '+
                 'FROM shopper_baskets '+
                 'INNER JOIN basket_contents ON shopper_baskets.basket_id = basket_contents.basket_id '+
                 'INNER JOIN products ON basket_contents.product_id = products.product_id '+
                 'INNER JOIN sellers ON basket_contents.seller_id = sellers.seller_id '+
                 'WHERE shopper_baskets.shopper_id = % s'% shopper_id)
# Queries

print(get_shopper_id(shopper_id))