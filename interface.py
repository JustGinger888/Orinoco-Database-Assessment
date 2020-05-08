def get_menu_choice():
    def print_menu(menu_options, title):       # Your menu design here

        print(title)
        print(73 * "-")
        for option in menu_options:
            print option

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu(menu_options, title)    # Displays menu
        choice = input("Enter your choice [1-5]: ")

        if choice == '1':
            int_choice = 1
            loop = False
        elif choice == '2':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter custom folder name(s). It may be a list of folder's names (example: c:,d:\docs): ")
            int_choice = 2
            loop = False
        elif choice == '3':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter a single filename of a file with custom folders list: ")
            int_choice = 3
            loop = False
        elif choice == '4':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter a single filename of a conf file: ")
            int_choice = 4
            loop = False
        elif choice == '5':
            int_choice = -1
            print("Exiting..")
            loop = False  # This will make the while loop to end
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again..")
    return [int_choice, choice]

title = 'ORINOCO - SHOPPER MAIN MENU'

menu_options = [
    '1) Display your order history',
    '2) Add an item to your basket',
    '3) View your basket',
    '4) Checkout',
    '5) Exit'
]


print(get_menu_choice())