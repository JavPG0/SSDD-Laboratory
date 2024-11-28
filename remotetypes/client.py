import sys
import Ice  # type: ignore
import RemoteTypes as rt  # Importa el módulo generado por Slice


def interact_with_iterable(iterable):
    """Interacción con un objeto remoto que implementa la interfaz Iterable."""
    print("Iterando sobre el objeto remoto:")
    while True:
        try:
            item = iterable.next()
            print(f"- {item}")
        except rt.StopIteration:
            print("Fin de la iteración.")
            break
        except rt.CancelIteration:
            print("La iteración fue cancelada debido a cambios en el objeto.")
            break


def interact_with_rset(rset):
    """Interacción con un RSet remoto."""
    while True:
        print("\nOperaciones para RSet:")
        print("1. Add")
        print("2. Remove")
        print("3. Length")
        print("4. Contains")
        print("5. Hash")
        print("6. Iterar")
        print("0. Salir")
        option = input("Elige una operación: ")

        if option == "1":
            item = input("Elemento a añadir: ")
            rset.add(item)
            print(f"Elemento '{item}' añadido.")
        elif option == "2":
            item = input("Elemento a eliminar: ")
            try:
                rset.remove(item)
                print(f"Elemento '{item}' eliminado.")
            except rt.KeyError:
                print("El elemento no existe en el conjunto.")
        elif option == "3":
            print(f"El conjunto tiene {rset.length()} elementos.")
        elif option == "4":
            item = input("Elemento a comprobar: ")
            print(f"El conjunto {'contiene' if rset.contains(item) else 'no contiene'} '{item}'.")
        elif option == "5":
            print(f"Hash del conjunto: {rset.hash()}.")
        elif option == "6":
            try:
                # Obtener el iterador remoto
                iterable = rset.iter()
                # Continuar obteniendo elementos hasta que termine
                while True:
                    item = iterable.next()  # Utiliza next directamente sobre el iterador
                    print(item)
            except rt.StopIteration:
                print("Fin de la iteración.")
            except rt.CancelIteration:
                print("La iteración fue cancelada debido a un cambio en el conjunto.")
            except Exception as e:
                print(f"Error inesperado: {str(e)}")
        elif option == "0":
            break
        else:
            print("Opción no válida.")



def interact_with_rlist(rlist):
    """Interacción con un RList remoto."""
    while True:
        print("\nOperaciones para RList:")
        print("1. Append")
        print("2. Pop")
        print("3. Get Item")
        print("4. Length")
        print("5. Hash")
        print("6. Iterar")
        print("0. Salir")
        option = input("Elige una operación: ")

        if option == "1":
            item = input("Elemento a añadir: ")
            rlist.append(item)
            print(f"Elemento '{item}' añadido.")
        elif option == "2":
            index = input("Índice (opcional, presiona Enter para omitir): ")
            if(index == ""): index = rlist.length() - 1
            try:
                if index:
                    print(f"Elemento eliminado: {rlist.pop(int(index))}.")
                else:
                    print(f"Elemento eliminado: {rlist.pop()}.")
            except rt.IndexError as ex:
                print(f"Error: {ex.message}")
        elif option == "3":
            index = int(input("Índice del elemento a obtener: "))
            try:
                print(f"Elemento en el índice {index}: {rlist.getItem(index)}.")
            except rt.IndexError as ex:
                print(f"Error: {ex.message}")
        elif option == "4":
            print(f"La lista tiene {rlist.length()} elementos.")
        elif option == "5":
            print(f"Hash de la lista: {rlist.hash()}.")
        elif option == "6":
            try:
                iterable = rlist.iter()
                while True:
                    item = iterable.next()
                    print(item)
            except rt.StopIteration:
                print("Fin de la iteración.")
            except rt.CancelIteration:
                print("La iteración fue cancelada debido a un cambio en la lista.")
            except Exception as e:
                print(f"Error inesperado: {str(e)}")
        elif option == "0":
            break
        else:
            print("Opción no válida.")


def interact_with_rdict(rdict):
    """Interacción con un RDict remoto."""
    while True:
        print("\nOperaciones para RDict:")
        print("1. Set Item")
        print("2. Get Item")
        print("3. Pop Item")
        print("4. Length")
        print("5. Hash")
        print("6. Iterar")
        print("0. Salir")
        option = input("Elige una operación: ")

        if option == "1":
            key = input("Clave: ")
            value = input("Valor: ")
            rdict.setItem(key, value)
            print(f"Par '{key}: {value}' añadido al diccionario.")
        elif option == "2":
            key = input("Clave: ")
            try:
                value = rdict.getItem(key)
                print(f"Valor para la clave '{key}': {value}.")
            except rt.KeyError as ex:
                print(f"Error: La clave '{key}' no existe.")
        elif option == "3":
            key = input("Clave a eliminar: ")
            try:
                print(f"Elemento eliminado: {rdict.pop(key)}.")
            except rt.KeyError as ex:
                print(f"Error: La clave '{key}' no existe.")
        elif option == "4":
            print(f"El diccionario tiene {rdict.length()} elementos.")
        elif option == "5":
            print(f"Hash del diccionario: {rdict.hash()}.")
        elif option == "6":
            try:
                iterable = rdict.iter()
                while True:
                    item = iterable.next()
                    print(item)
            except rt.StopIteration:
                print("Fin de la iteración.")
            except rt.CancelIteration:
                print("La iteración fue cancelada debido a un cambio en el diccionario.")
            except Exception as e:
                print(f"Error inesperado: {str(e)}")
        elif option == "0":
            break
        else:
            print("Opción no válida.")


def main():
    """Principal method main of the client class, which interacts with the server."""
    if len(sys.argv) != 2:
        print("Uso: python client.py \"factory -t -e 1.1:tcp -h <host> -p <port> -t <timeout>\"")
        return

    proxy_string = sys.argv[1]

    try:
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy(proxy_string)
            factory = rt.FactoryPrx.checkedCast(base)
            if not factory:
                print("No se pudo castear el proxy a rt.FactoryPrx.")
                return

            print("Conexión con 'factory' exitosa.")

            while True:
                print("\nSelecciona el tipo de objeto:")
                print("1. RSet")
                print("2. RList")
                print("3. RDict")
                print("0. Salir")
                choice = input("Opción: ")

                if choice == "1":
                    identifier = input("Identificador para RSet: ")
                    rset = rt.RSetPrx.checkedCast(factory.get(rt.TypeName.RSet, identifier))
                    if rset:
                        interact_with_rset(rset)
                    else:
                        print("No se pudo obtener el proxy para RSet.")
                elif choice == "2":
                    identifier = input("Identificador para RList: ")
                    rlist = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, identifier))
                    if rlist:
                        interact_with_rlist(rlist)
                    else:
                        print("No se pudo obtener el proxy para RList.")
                elif choice == "3":
                    identifier = input("Identificador para RDict: ")
                    rdict = rt.RDictPrx.checkedCast(factory.get(rt.TypeName.RDict, identifier))
                    if rdict:
                        interact_with_rdict(rdict)
                    else:
                        print("No se pudo obtener el proxy para RDict.")
                elif choice == "0":
                    print("Saliendo...")
                    break
                else:
                    print("Opción no válida.")

    except Exception as ex:
        print(f"Error al conectar con el servidor: {ex}")


if __name__ == "__main__":
    main()
