import json
from typing import Optional, Dict

import RemoteTypes as rt  # Asegúrate de que esté correctamente importado
import hashlib
from remotetypes.iterable import RemoteIterator

class RemoteDict(rt.RDict):
    """Clase que implementa un diccionario remoto con persistencia."""

    def __init__(self, identifier: str = None) -> None:
        """
        Inicializa un diccionario remoto.

        :param identifier: Identificador único para la persistencia.
        """
        self.identifier = identifier or "default_dict"  # Nombre por defecto si no se proporciona uno
        self.storage: Dict[str, str] = {}
        self.file_path = f"{identifier}_dict.json"
        self._load()  # Carga los datos persistidos si existen

    def _log(self, action: str) -> None:
        """Log an action related to the JSON file."""
        print(f"[RemoteDict] {action} archivo: {self.file_path}")

    def _save(self) -> None:
        """Guarda el diccionario actual en un archivo JSON."""

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.storage, file)
        self._log("Datos guardados en")

    def _load(self) -> None:
        """Carga el diccionario desde un archivo JSON, si existe."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.storage = json.load(file)
            self._log("Cargado desde")
        except FileNotFoundError:
            self._log("Creado")

    def setItem(self, key: str, item: str, current: Optional[rt.Ice.Current] = None) -> None:
        """
        Establece un valor en el diccionario remoto con una clave específica.

        :param key: Clave para el valor.
        :param item: Valor a asociar con la clave.
        """
        self.storage[key] = item
        self._save()
        self._log(f"Elemento añadido: {key} -> {item} en")

    def remove(self, item: str, current: Optional[rt.Ice.Current] = None) -> None:
        """
        Elimina un valor del diccionario remoto.

        :param item: Valor a eliminar.
        :raises rt.KeyError: Si la clave no existe.
        """
        if item in self.storage:
            del self.storage[item]
            self._save()
            self._log(f"Elemento eliminado: {item} de")
        else:
            raise rt.KeyError(key=item)

    def getItem(self, key: str, current: Optional[rt.Ice.Current] = None) -> str:
        """
        Obtiene un valor del diccionario remoto usando la clave.

        :param key: Clave del valor a recuperar.
        :return: El valor asociado a la clave.
        :raises rt.KeyError: Si la clave no existe.
        """
        if key in self.storage:
            return self.storage[key]
        else:
            raise rt.KeyError(key=key)

    def contains(self, key: str, current: Optional[rt.Ice.Current] = None) -> bool:
        """
        Verifica si una clave existe en el diccionario remoto.

        :param key: Clave a buscar.
        :return: True si la clave existe, False en caso contrario.
        """
        return key in self.storage

    def length(self, current: Optional[rt.Ice.Current] = None) -> int:
        """
        Devuelve el número de elementos en el diccionario remoto.

        :return: Número de elementos.
        """
        return len(self.storage)

    def iter(self, current: Optional[rt.Ice.Current] = None) -> rt.IterablePrx:
        """
        Devuelve un iterador remoto para recorrer el diccionario.

        :return: Proxy de un iterador remoto.
        """
        servant = RemoteIterator(self.storage)  # Pasa los pares clave-valor al iterador
        proxy = current.adapter.addWithUUID(servant)  # Registra el iterador en el adaptador
        return rt.IterablePrx.uncheckedCast(proxy)

    def pop(self, key: str, current: Optional[rt.Ice.Current] = None) -> str:
        """Elimina un ítem del diccionario por su clave y devuelve el valor."""
        if key in self.storage:
            value = self.storage.pop(key)  # Elimina el ítem y devuelve el valor
            self._save()  # Guarda los cambios
            return value
        else:
            raise rt.KeyError(key=key)  # Lanza KeyError si la clave no existe
        
    def hash(self, current: Optional[rt.Ice.Current] = None) -> int:
        """Calcula y devuelve un hash único reducido para el diccionario."""
        # Convierte los elementos del diccionario a una cadena ordenada
        items = "".join(f"{key}:{value}" for key, value in sorted(self.storage.items()))
        # Calcula el hash SHA-256
        hash_hex = hashlib.sha256(items.encode('utf-8')).hexdigest()
        # Convierte el hash hexadecimal en un entero y reduce el tamaño
        hash_int = int(hash_hex, 16)
        return hash_int % (2**31 - 1)  # Reduce el entero para que sea manejable por Ice