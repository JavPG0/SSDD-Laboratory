from typing import Optional
import Ice  # type: ignore
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
#from remotetypes.iterable import DictIterable


class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict."""

    def __init__(self, identifier: str) -> None:
        """Initialise a RemoteDict with an empty StringSet."""
        self._storage = StringSet()  # Usamos StringSet para las claves
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        """Set an item in the StringSet dictionary."""
        self._storage.add(key)  # Almacenamos las claves en el StringSet, sin valores

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Get an item from the StringSet dictionary."""
        if key in self._storage:
            return self._storage[key]  # Devolvemos el valor asociado a la clave
        raise rt.KeyError(key)

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Pop an item from the StringSet dictionary."""
        try:
            self._storage.remove(key)
            return key  # El valor devuelto es la clave eliminada
        except KeyError as exc:
            raise rt.KeyError(key) from exc

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of items in the StringSet dictionary."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the StringSet contains an item."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash for the StringSet dictionary."""
        contents = sorted(self._storage)
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object for the StringSet dictionary."""
        #adapter = current.adapter
        #servant = DictIterable(self._storage)
        #proxy = adapter.addWithUUID(servant)
        #return rt.IterablePrx.checkedCast(proxy)

