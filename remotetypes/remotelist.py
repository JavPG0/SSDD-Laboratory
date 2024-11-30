import json
from typing import Optional
import Ice  # type: ignore
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
from remotetypes.iterable import RemoteIterator


class RemoteList(rt.RList):
    """Implementation of the remote interface RList with persistence."""

    #Initialize a RemoteList with an empty or loaded StringSet.
    def __init__(self, identifier: str) -> None:
        """Initialize a RemoteList with an empty or loaded StringSet."""
        self.id_ = identifier
        self.file_path = f"{identifier}_list.json"
        self._storage = self._load()

    #Log an action related to the JSON file.
    def _log(self, action: str) -> None:
        """Log an action related to the JSON file."""
        print(f"[RemoteList] {action} archivo: {self.file_path}")

    #Save the current storage to a JSON file
    def _save(self) -> None:
        """Save the current storage to a JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(list(self._storage), f)
        self._log("Datos guardados en")

    #Load the storage from a JSON file, or initialize a new one if the file doesn't exist.
    def _load(self) -> StringSet:
        """Load the storage from a JSON file, or initialize a new one if the file doesn't exist."""
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            self._log("Cargado desde")
            return StringSet(data)
        except (FileNotFoundError, json.JSONDecodeError):
            self._log("Creado")
            return StringSet()

    #Return the identifier of the object.
    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    #Append an item to the StringSet.
    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Append an item to the StringSet."""
        self._storage.add(item)
        self._save()
        self._log(f"Elemento añadido: {item} en")

    #Remove an item from the StringSet.
    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet."""
        try:
            self._storage.remove(item)
            self._save()
        except KeyError as exc:
            raise rt.KeyError(item) from exc

    #Return the length of the StringSet.
    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the length of the StringSet."""
        return len(self._storage)

    #Check if the object contains an item.
    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the object contains an item."""
        return item in self._storage

    #Calculate a hash.
    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash."""
        contents = list(self._storage)
        contents.sort()
        return hash(repr(contents))

    #Create an iterable object for the StringSet.
    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object for the StringSet."""
        servant = RemoteIterator(self._storage)
        proxy = current.adapter.addWithUUID(servant)
        return rt.IterablePrx.uncheckedCast(proxy)

    #Get an item from the remotelist, without remove it.
    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Get an item from the remotelist, without remove it."""
        try:
            return list(self._storage)[index]
        except IndexError as exc:
            raise rt.IndexError("Index out of range") from exc

    #Remove and return an element from the storage.
    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            storage_list = list(self._storage)
            if index is None:
                item = storage_list.pop()  # Remove last item
            else:
                item = storage_list.pop(index)
            self._storage = StringSet(storage_list)  # Update storage
            self._save()
            return item
        except IndexError as exc:
            raise rt.IndexError("Index out of range") from exc

