
from typing import Optional, Iterable
import Ice  # type: ignore
import RemoteTypes as rt
from remotetypes.customset import StringSet  # noqa: F401; pylint: disable=import-error

class RemoteIterator(rt.Iterable):
    """Implementation of the remote interface Iterable."""
    def __init__(self, rset):
        self._rset = rset
        self._iterator = iter(self._rset.items)  # Crea un iterador sobre los elementos del conjunto

    def __next__(self):
        try:
            return next(self._iterator)  # Devuelve el siguiente elemento
        except StopIteration:
            raise rt.StopIteration()  # Lanza StopIteration cuando no hay más elementos