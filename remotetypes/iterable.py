import Ice
import RemoteTypes as rt  # Asegúrate de que esté correctamente importado
from typing import Optional


class RemoteIterator(rt.Iterable):
    """Iterador remoto para los objetos RSet, RList y RDict."""
    
    def __init__(self, collection) -> None:
        """Inicializa el iterador con una colección."""
        self._collection = collection  # Recibe la colección (StringSet, RList, RDict)
        self._iterator = iter(self._collection)  # Crea un iterador sobre la colección

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Devuelve el siguiente elemento de la colección."""
        try:
            return next(self._iterator)  # Devuelve el siguiente elemento
        except StopIteration as exc:
            raise rt.StopIteration() from exc  # Lanza StopIteration si ya no hay elementos
        except RuntimeError as exc:
            raise rt.CancelIteration() from exc  # Lanza CancelIteration si la colección se modifica
