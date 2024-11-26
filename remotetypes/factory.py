from typing import Optional
import Ice  # type: ignore
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

from remotetypes.remoteset import RemoteSet
from remotetypes.remotelist import RemoteList
from remotetypes.remotedict import RemoteDict


class Factory(rt.Factory):
    """Factory class to create instances of remote objects."""

    def __init__(self) -> None:
        """Initialize the factory with an empty storage for objects."""
        self._storage = {}

    def get(self, typeName: rt.TypeName, identifier: Optional[str] = None, current: Optional[Ice.Current] = None) -> rt.RTypePrx:
        """Create or return an object of the requested type."""
        if identifier is None:
            raise ValueError("Identifier cannot be None")

        if identifier in self._storage:
            return self._storage[identifier]

        # Create a new object based on the requested type
        adapter = current.adapter
        if typeName == rt.TypeName.RSet:
            servant = RemoteSet(identifier)
        elif typeName == rt.TypeName.RList:
            servant = RemoteList(identifier)
        elif typeName == rt.TypeName.RDict:
            servant = RemoteDict(identifier)
        else:
            raise ValueError(f"Unknown type: {typeName}")

        # Add the servant to the adapter and return its proxy
        proxy = adapter.addWithUUID(servant)
        self._storage[identifier] = rt.RTypePrx.checkedCast(proxy)
        return self._storage[identifier]
