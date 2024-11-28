import json
from typing import Optional
from remotetypes.iterable import RemoteIterator
import Ice  # type: ignore
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

from remotetypes.customset import StringSet


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet with persistence."""

    def __init__(self, identifier: str) -> None:
        """Initialize a RemoteSet with an empty or loaded StringSet."""
        self.id_ = identifier
        self.file_path = f"{identifier}_set.json"
        self._storage_ = self._load()

    def _log(self, action: str) -> None:
        """Log an action related to the JSON file."""
        print(f"[RemoteSet] {action} archivo: {self.file_path}")

    def _save(self) -> None:
        """Save the current storage to a JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(list(self._storage_), f)
        self._log("Datos guardados en")

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

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
            self._save()
            self._log(f"Elemento eliminado: {item} de ")    
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        adapter = current.adapter
        servant = RemoteIterator(self._storage_)
        proxy = adapter.addWithUUID(servant)
        return rt.IterablePrx.checkedCast(proxy)

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new string to the StringSet."""
        self._storage_.add(item)
        self._save()
        self._log(f"Elemento añadido: {item} en")


    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            item = self._storage_.pop()
            self._save()
            return item
        except KeyError as exc:
            raise rt.KeyError() from exc                                                          
