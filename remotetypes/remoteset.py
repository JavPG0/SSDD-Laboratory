"""Needed classes to implement and serve the RSet type."""
import json
from typing import Optional
from remotetypes.iterable import RemoteIterator
import Ice  
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    #Initialise a RemoteSet with an empty StringSet.
    def __init__(self, identifier) -> None:
        """Initialise a RemoteSet with an empty StringSet."""
        self._storage_ = StringSet()
        self.file_path = f"{identifier}_set.json"
        self.id_ = identifier

    #Log an action related to the JSON file.
    def _log(self, action: str) -> None:
        """Log an action related to the JSON file."""
        print(f"[RemoteSet] {action} archivo: {self.file_path}")

    #Save the current storage to a JSON file
    def _save(self) -> None:
        """Save the current storage to a JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(list(self._storage_), f)
        self._log("Datos guardados en")

    #Load the storage from a JSON file, or initialize a new one if the file doesn't exist.
    def _load(self) -> StringSet:
        """Load the storage from a JSON file, or initialize a new one if the file doesn't exist."""
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            self._log("Cargado")
            return StringSet(data)
        except (FileNotFoundError, json.JSONDecodeError):
            self._log("Creado")
            return StringSet()

    #Return the identifier of the object.    
    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    #Remove an item from the StringSet if added. Else, raise a remote exception.
    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
            self._save()
            self._log(f"Elemento eliminado:{item}  de")
        except KeyError as error:
            raise rt.KeyError(item) from error

    #Return the number of elements in the StringSet.
    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    #Check the pertenence of an item to the StringSet.
    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    #Calculate a hash from the content of the internal StringSet.
    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    #Create an iterable object.
    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        adapter = current.adapter
        servant = RemoteIterator(self._storage_)
        proxy = adapter.addWithUUID(servant)
        return rt.IterablePrx.checkedCast(proxy)
    
    #Add a new string to the StringSet.
    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new string to the StringSet."""
        self._storage_.add(item)
        self._save()
        self._log(f"Elemento añadido: {item} en")

    #Remove and return an element from the storage.
    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            item = self._storage_.pop()
            self._save()
            self._log("Elemento {item} eliminado de")
            return item
        except KeyError as exc:
            raise rt.KeyError() from exc