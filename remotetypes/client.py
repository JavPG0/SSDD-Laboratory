import sys
import Ice  # type: ignore
import RemoteTypes as rt  # Importa el módulo generado por Slice

# Display the menu of operations for an RSet object.
def showRsetOptions() -> int:
    print("\nOperations for RSet:")
    print("1. Add")
    print("2. Remove")
    print("3. Length")
    print("4. Contains")
    print("5. Hash")
    print("6. Iterate")
    print("0. Exit")
    return input("Choose an operation: ")

# Interact with a remote RSet object.
def interactWithRset(rset):
    while True:     #The user will be able to perform operations with rset until he chooses option 0 (break).
        option = showRsetOptions()  #Take the value that indicates the option chosen by the user.


        # Evaluate the operation in terms of the option.
        if option == "1": #Add
            item = input("Item to add: ")
            rset.add(item)
            print(f"Item '{item}' added.")
        elif option == "2": #Remove
            item = input("Item to remove: ")
            try:
                rset.remove(item)
                print(f"Item '{item}' removed.")
            except rt.KeyError:
                print("The item does not exist in the set.")
        elif option == "3": #Lenght
            print(f"The set contains {rset.length()} items.")
        elif option == "4": #Contains
            item = input("Item to check: ")
            print(f"The set {'contains' if rset.contains(item) else 'does not contain'} '{item}'.")
        elif option == "5": #Hash
            print(f"Set hash: {rset.hash()}.")
        elif option == "6": #Iterable
            try:
                iterable = rset.iter()
                while True:
                    item = iterable.next()
                    print(item)
            except rt.StopIteration:
                print("End of iteration.")
            except rt.CancelIteration:
                print("The iteration was canceled due to a change in the set.")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
        elif option == "0": #Exit
            break
        else:
            print("Invalid option.")

# Obtain and interact with an RSet from the factory
def selectionRset(factory)-> None:  #If the user decides to operate with rset, we capture the identifier requested, operate with the proxy and display the operations.
    identifier = input("Identifier for RSet: ")
    rset = rt.RSetPrx.checkedCast(factory.get(rt.TypeName.RSet, identifier))    # Retrieves a type-safe proxy to interact with a remote RSet identified by 'identifier'.
    if rset:
        interactWithRset(rset)
    else:
        print("Could not obtain the proxy for RSet.")

# Display the menu of operations for an RList object
def showRlistOptions() -> int:
    print("\nOperations for RList:")
    print("1. Append")
    print("2. Pop")
    print("3. Get Item")
    print("4. Length")
    print("5. Hash")
    print("6. Iterate")
    print("0. Exit")
    return input("Choose an operation: ")

# Interact with a remote RList object
def interactWithRlist(rlist):
    while True:  #The user will be able to perform operations with rlist until he chooses option 0 (break).
        option = showRlistOptions() #Take the value that indicates the option chosen by the user.

        # Evaluate the operation in terms of the option.
        if option == "1":   #Append
            item = input("Item to append: ")
            rlist.append(item)
            print(f"Item '{item}' appended.")
        elif option == "2": #pop
            index = input("Index (optional, press Enter to skip): ")
            if(index == ""): index = rlist.length() - 1
            try:
                if index:
                    print(f"Item removed: {rlist.pop(int(index))}.")
                else:
                    print(f"Item removed: {rlist.pop()}.")
            except rt.IndexError as ex:
                print(f"Error: {ex.message}")
        elif option == "3": #Get Item
            index = int(input("Index of the item to get: "))
            try:
                print(f"Item at index {index}: {rlist.getItem(index)}.")
            except rt.IndexError as ex:
                print(f"Error: {ex.message}")
        elif option == "4": #Length
            print(f"The list contains {rlist.length()} items.")
        elif option == "5": #Hash
            print(f"List hash: {rlist.hash()}.")
        elif option == "6": #Iterate
            try:
                iterable = rlist.iter()
                while True:
                    item = iterable.next()
                    print(item)
            except rt.StopIteration:
                print("End of iteration.")
            except rt.CancelIteration:
                print("The iteration was canceled due to a change in the list.")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
        elif option == "0": #Exit
            break
        else:
            print("Invalid option.")

# Obtain and interact with an RList from the factory
def selectionRlist(factory) -> None:    #If the user decides to operate with rlist, we capture the identifier requested, operate with the proxy and display the operations.
    identifier = input("Identifier for RList: ")
    rlist = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, identifier)) # Retrieves a type-safe proxy to interact with a remote RSet identified by 'identifier'.
    if rlist:
        interactWithRlist(rlist)
    else:
        print("Could not obtain the proxy for RList.")

# Display the menu of operations for an RDict object
def showRdictOptions() -> int:
    print("\nOperations for RDict:")
    print("1. Set Item")
    print("2. Get Item")
    print("3. Pop Item")
    print("4. Length")
    print("5. Hash")
    print("6. Iterate")
    print("0. Exit")
    return input("Choose an operation: ")

# Interact with a remote RDict object
def interactWithRdict(rdict):
    while True: #The user will be able to perform operations with rdict until he chooses option 0 (break).
        option = showRdictOptions() #Take the value that indicates the option chosen by the user.
    
        # Evaluate the operation in terms of the option.
        if option == "1":   #Set item
            key = input("Key: ")
            value = input("Value: ")
            rdict.setItem(key, value)
            print(f"Pair '{key}: {value}' added to the dictionary.")
        elif option == "2": #Get item
            key = input("Key: ")
            try:
                value = rdict.getItem(key)
                print(f"Value for key '{key}': {value}.")
            except rt.KeyError as ex:
                print(f"Error: The key '{key}' does not exist.")
        elif option == "3": #Pop item
            key = input("Key to remove: ")
            try:
                print(f"Item removed: {rdict.pop(key)}.")
            except rt.KeyError as ex:
                print(f"Error: The key '{key}' does not exist.")
        elif option == "4": #Lenght
            print(f"The dictionary contains {rdict.length()} items.")
        elif option == "5": #Hash
            print(f"Dictionary hash: {rdict.hash()}.")
        elif option == "6": #Iterate
            try:
                iterable = rdict.iter()
                while True:
                    item = iterable.next()
                    print(item)
            except rt.StopIteration:
                print("End of iteration.")
            except rt.CancelIteration:
                print("The iteration was canceled due to a change in the dictionary.")
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
        elif option == "0": #Exit
            break
        else:
            print("Invalid option.")

# Obtain and interact with an RDict from the factory
def selectionRdict(factory) -> None:    #If the user decides to operate with rdict, we capture the identifier requested, operate with the proxy and display the operations.
    identifier = input("Identifier for RDict: ")
    rdict = rt.RDictPrx.checkedCast(factory.get(rt.TypeName.RDict, identifier)) # Retrieves a type-safe proxy to interact with a remote Rdict identified by 'identifier'.
    if rdict:
        interactWithRdict(rdict)
    else:
        print("Could not obtain the proxy for RDict.")

# Display the main menu of object types to interact with
def optionsMain() -> int:
    print("\nSelect the object type:")
    print("1. RSet")
    print("2. RList")
    print("3. RDict")
    print("0. Exit")
    return input("Option: ")

# Main client method to interact with the server
def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py \"factory -t -e 1.1:tcp -h <host> -p <port> -t <timeout>\"")
        return

    proxy_string = sys.argv[1]

    try:
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy(proxy_string)
            factory = rt.FactoryPrx.checkedCast(base)
            if not factory:
                print("Could not connect to 'factory'. Please check the input.")
                return

            print("Connection to 'factory' successful.")

            while True:
                option = optionsMain()

                if option == "1": selectionRset(factory)
                elif option == "2": selectionRlist(factory)
                elif option == "3": selectionRdict(factory)
                elif option == "0": break
                else: print("Invalid option.")

    except Exception as ex:
        print(f"Error connecting to the server: {ex}")

if __name__ == "__main__":
    main()
