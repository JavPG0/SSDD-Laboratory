import json
from typing import Optional, Dict

import RemoteTypes as rt   
import hashlib
from remotetypes.iterable import RemoteIterator


class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict."""

    #Initialises the remote dict dictionary
    def __init__(self, identifier: str = None) -> None:
        """ Initialises the remote dict dictionary  """

        self.identifier = identifier or "default_dict"
        self.storage: Dict[str, str] = {}
        self.file_path = f"{identifier}_dict.json"
        self._load()

    #Log an action related to the JSON file.
    def _log(self, action: str) -> None:
        """Log an action related to the JSON file."""

        print(f"[RemoteDict] {action} archivo: {self.file_path}")

    #Saves the current dictionary to a JSON file
    def _save(self) -> None:
        """Saves the current dictionary to a JSON file"""

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.storage, file)
            self._log("Datos guardados en")
        except IOError as e:
            self._log(f"Error al guardar datos: {e}")

    #Loads the dictionary from a JSON file, if it exists
    def _load(self) -> None:
        """Loads the dictionary from a JSON file, if it exists"""

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.storage = json.load(file)
            self._log("Cargado desde")
        except FileNotFoundError:
            self._log("Creado")
        except json.JSONDecodeError as e:
            self._log(f"Error al cargar datos: {e}")
    
    #Return the identifier of the object
    def identifier(self, current: Optional[rt.Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.identifier

    #Sets a value in the remote dictionary to a specific key.
    def setItem(self, key: str, item: str, current: Optional[rt.Ice.Current] = None) -> None:
        """Sets a value in the remote dictionary to a specific key."""

        if not key:
            raise ValueError("La clave no puede ser una cadena vacía.")
        if not item:
            raise ValueError("El valor no puede ser una cadena vacía.")
        self.storage[key] = item
        self._save()
        self._log(f"Elemento añadido: {key} -> {item} en")

    #Deletes a value from the remote dictionary
    def remove(self, item: str, current: Optional[rt.Ice.Current] = None) -> None:
        """Deletes a value from the remote dictionary."""

        if item in self.storage:
            del self.storage[item]
            self._save()
            self._log(f"Elemento eliminado: {item} de")
        else:
            raise rt.KeyError(key=item)

    #Gets a value from the remote dictionary using the key
    def getItem(self, key: str, current: Optional[rt.Ice.Current] = None) -> str: 
        """Gets a value from the remote dictionary using the key."""

        if key in self.storage:
            return self.storage[key]
        else:
            raise rt.KeyError(key=key)

    #Checks if a key exists in the remote dictionary
    def contains(self, key: str, current: Optional[rt.Ice.Current] = None) -> bool:
        """Checks if a key exists in the remote dictionary."""

        return key in self.storage

    #Returns the number of items in the remote dictionary
    def length(self, current: Optional[rt.Ice.Current] = None) -> int:
        """Returns the number of items in the remote dictionary."""

        return len(self.storage)

    #Create an iterable object.
    def iter(self, current: Optional[rt.Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""

        servant = RemoteIterator(self.storage)
        proxy = current.adapter.addWithUUID(servant)
        return rt.IterablePrx.uncheckedCast(proxy)

    #Remove and return an element from the storage.
    def pop(self, key: str, current: Optional[rt.Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""

        if key in self.storage:
            value = self.storage.pop(key)
            self._save()
            return value
        else:
            raise rt.KeyError(key=key)

    #Calculates and returns a unique reduced hash for the dictionary
    def hash(self, current: Optional[rt.Ice.Current] = None) -> int:
        """Calculates and returns a unique reduced hash for the dictionary."""

        contents = list(self.storage)
        contents.sort()
        return hash(repr(contents))