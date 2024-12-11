import json
from typing import Optional, Dict
import Ice  # Importa el módulo Ice directamente
import RemoteTypes as rt
import hashlib
from remotetypes.iterable import RemoteIterator


class RemoteDict(rt.RDict):
    """Implementation of the remote interface RDict."""

    def __init__(self, identifier: str = None) -> None:
        self.identifier = identifier or "default_dict"
        self.storage: Dict[str, str] = {}
        self.file_path = f"{identifier}_dict.json"
        self._load()

    def _log(self, action: str) -> None:
        print(f"[RemoteDict] {action} archivo: {self.file_path}")

    def _save(self) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.storage, file)
            self._log("Datos guardados en")
        except IOError as e:
            self._log(f"Error al guardar datos: {e}")

    def _load(self) -> None:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.storage = json.load(file)
            self._log("Cargado desde")
        except FileNotFoundError:
            self._log("Creado")
        except json.JSONDecodeError as e:
            self._log(f"Error al cargar datos: {e}")

    def identifier(self, current: Optional[Ice.Current] = None) -> str:  # Cambiado a Ice.Current
        return self.identifier

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        if not key:
            raise ValueError("La clave no puede ser una cadena vacía.")
        if not item:
            raise ValueError("El valor no puede ser una cadena vacía.")
        self.storage[key] = item
        self._save()
        self._log(f"Elemento añadido: {key} -> {item} en")

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        if item in self.storage:
            del self.storage[item]
            self._save()
            self._log(f"Elemento eliminado: {item} de")
        else:
            raise rt.KeyError(key=item)

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self.storage:
            return self.storage[key]
        else:
            raise rt.KeyError(key=key)

    def contains(self, key: str, current: Optional[Ice.Current] = None) -> bool:
        return key in self.storage

    def length(self, current: Optional[Ice.Current] = None) -> int:
        return len(self.storage)

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        servant = RemoteIterator(self.storage)
        proxy = current.adapter.addWithUUID(servant)
        return rt.IterablePrx.uncheckedCast(proxy)

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        if key in self.storage:
            value = self.storage.pop(key)
            self._save()
            return value
        else:
            raise rt.KeyError(key=key)

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        contents = list(self.storage)
        contents.sort()
        return hash(repr(contents))
