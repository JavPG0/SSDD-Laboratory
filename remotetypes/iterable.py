import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from typing import Optional


class RemoteIterator(rt.Iterable):
    """Remote Iterator for RSet, RList and RDict objects."""
    
    #Initialises the iterator with a collection.
    def __init__(self, collection) -> None:
        """Initialises the iterator with a collection."""
        self._collection = collection  # Recibe la colección (StringSet, RList, RDict)
        self._iterator = iter(self._collection)  # Crea un iterador sobre la colección

    #Returns the next item in the collection.
    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Returns the next item in the collection."""
        try:
            return next(self._iterator)  # Devuelve el siguiente elemento
        except StopIteration as exc:
            raise rt.StopIteration() from exc  # Lanza StopIteration si ya no hay elementos
        except RuntimeError as exc:
            raise rt.CancelIteration() from exc  # Lanza CancelIteration si la colección se modifica
