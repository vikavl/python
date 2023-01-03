import collections

# contact structure as namedtuple from collections
Contact = collections.namedtuple("Contact", ["name", "number"])

# list of contacts
contacts = []

# decorator 
def input_error(func):
    def inner(*args):
        try: 
            func(*args)
        # Handling an error occured, 
        # when there are no commands in dict such was inputted.
        except KeyError as e:
            print("No such a command? Try again...")
            # I don't understand the reason, 
            # but on that point bot is closing, 
            # so I have to "run" him again
            main()
        # Handling validation exceptions for fields "name" and "number".
        except ValueError as e:
            print(e)
        # Handling an exception in cases:
        # 1. There is no desired contact in the contacts list.
        # 2. Contacts list is empty.
        except IndexError as e:
            print(e)
        # Used when user skipping arguments for some commands.
        # E.g.:
        # Enter command>add n
        # add() missing 1 required positional argument: 'number'
        except TypeError as e:
            print(e)
    return inner

# Validation of field "name"
def name_validation(name):
    if name.isalnum() == False:
        raise ValueError("Name is not valid (should be alphanumeric). Try again!")
    return name

# Validation of field "number"
def number_validation(number):
    if len(number) < 9 or number.isdigit() == False:
        raise ValueError("Phone number is not valid (should be numerical and have 9 numbers in it). Try again!")
    return int(number)

# bot's "hello" command
def hello(): print("How can I help you?")

# bot's "add" command
# used annotation of decorator "input_error" to handle exception occured
@input_error
def add(name, number, flag=True):
    name = name_validation(name)
    number = number_validation(number)
    contact = Contact(name, number)
    contacts.append(contact)
    # flag is used for 2 different commands outputs
    # for "add" command:
    if flag: 
        print(f"Contact is added: {contact}")
    # for "change" command:
    else:
        print(f"Contact is updated: {contact}")

# bot's "change" command
# used annotation of decorator "input_error" to handle exception occured
@input_error
def change(name, number):
    # 1. find contact with defined name (its index in the list)
    # 2. delete contact from list (by found index)
    # 3. add updated contact to the list (using "add" function)
    index_to_remove_contact = None
    for i in range(len(contacts)):
        if contacts[i].name == name: 
            index_to_remove_contact = i
            break
    if index_to_remove_contact is not None:
        contacts.pop(index_to_remove_contact)
        add(name, number, False)
    # case: if there is no contact with inputted "name"
    else:
        raise IndexError(f"No contact with name: {name}")

# bot's "phone" command
# used annotation of decorator "input_error" to handle exception occured
@input_error
def phone(name):
    if contacts:
        result = None
        for c in contacts:
            if c.name == name:
                result = c
        if result is not None:
            print(f"Contact details: {result}")
        else:
            raise IndexError(f"No contact with name: {name}") 
    else:
        raise IndexError("Contact list is empty. Add some contacts to start chatting:)")

# bot's "show_all" command
# used annotation of decorator "input_error" to handle exception occured
@input_error
def show_all():
    if contacts:
        for c in contacts:
            print(c)
    else:
        raise IndexError("Contact list is empty. Add some contacts to start chatting:)")

# dictionary of commands 
commands_dict = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all,
    # at these case - close bot
    "good bye": "ciao",
    "close": "ciao",
    "exit": "ciao",
    ".": "ciao",
}

# used annotation of decorator "input_error" to handle exception occured
@input_error
def main():
    while True:
        command = input("Enter command>").strip()
        splitted_command = command.split()
        if len(splitted_command) >= 2 and (
            splitted_command[0].lower() == "add" or
            splitted_command[0].lower() == "change" or
            splitted_command[0].lower() == "phone"):
            commands_dict[splitted_command[0].lower()](*splitted_command[1:])
        else:
            if commands_dict[command.lower()] == "ciao":
                break
            commands_dict[command.lower()]()

if __name__ == "__main__":
    main()


