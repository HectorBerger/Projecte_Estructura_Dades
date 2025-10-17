# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""
import os
import cfg

class ImageID:
    def __init__(self):
        # Mapes bidireccionals per consultes eficients
        self._file2uuid = {}  # rel_path_canon (str) -> uuid_str
        self._uuid2file = {}  # uuid_str -> rel_path_canon (str)

    def _to_rel_canonical(self, file: str) -> str:
        abs_path = file if os.path.isabs(file) else os.path.join(cfg.get_root(), file)
        abs_path = os.path.realpath(abs_path)
        return cfg.get_canonical_pathfile(abs_path)

    def generate_uuid(self, file: str) -> str | None:
        rel_path = self._to_rel_canonical(file)

        # Ja registrat per aquest fitxer
        if rel_path in self._file2uuid:
            return self._file2uuid[rel_path]

        # UUID determinista basat en el path relatiu canònic
        uuid_obj = cfg.get_uuid(rel_path)  # requerit per l’enunciat
        uuid_str = str(uuid_obj)

        # Col·lisió improbable: mateix uuid assignat a un altre fitxer
        other = self._uuid2file.get(uuid_str)
        if other is not None and other != rel_path:
            print(f"ERROR: Col·lisió UUID: {uuid_str} ja assignat a {other}")
            return None

        # Registra
        self._file2uuid[rel_path] = uuid_str
        self._uuid2file[uuid_str]  = rel_path
        return uuid_str

    def get_uuid(self, file: str) -> str | None:
        """Retorna l'UUID (str) associat a 'file' si existeix, altrament None."""
        rel_path = self._to_rel_canonical(file)
        return self._file2uuid.get(rel_path)

    def remove_uuid(self, uuid: str) -> None:
        """Elimina el UUID del registre; si no existeix, no fa res."""
        rel_path = self._uuid2file.pop(uuid, None)
        if rel_path is not None:
            self._file2uuid.pop(rel_path, None)