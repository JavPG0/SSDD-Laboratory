from typing import Optional
import Ice  # type: ignore
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
#from remotetypes.iterable import ListIterable


class RemoteList(rt.RList):
    """Implementation of the remote interface RList."""

    def __init__(self, identifier: str) -> None:
        """Initialise a RemoteList with an empty StringSet."""
        self._storage = StringSet()  # Usamos StringSet en lugar de lista normal
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Append an item to the StringSet."""
        self._storage.add(item)

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet."""
        try:
            self._storage.remove(item)
        except KeyError as exc:
            raise rt.KeyError(item) from exc

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the length of the StringSet."""
        return len(self._storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if the StringSet contains an item."""
        return item in self._storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash for the StringSet."""
        contents = list(self._storage)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object for the StringSet."""
        #adapter = current.adapter
        #servant = ListIterable(self._storage)
        #proxy = adapter.addWithUUID(servant)
        #return rt.IterablePrx.checkedCast(proxy)
        
        

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Get an item from the StringSet."""
        try:
            return list(self._storage)[index]
        except IndexError as exc:
            raise rt.IndexError("Index out of range") from exc

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """Pop an item from the StringSet."""
        try:
            # Convert StringSet to list to use pop, since it's not ordered
            storage_list = list(self._storage)
            if index is None:
                return storage_list.pop()  # Remove last item
            return storage_list.pop(index)
        except IndexError as exc:
            raise rt.IndexError("Index out of range") from exc
