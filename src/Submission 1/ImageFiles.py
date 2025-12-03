# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import os
import cfg

class ImageFiles:
    def __init__(self):
        self._prev = set()
        self._added = []
        self._removed = []

    """
    def reload_fs(self, path: str = None) -> None:
        # Directori arrel
        if path is None:
            root = cfg.get_root()
        else:
            # Si és relatiu, l’enganxem a ROOT_DIR
            root = path
            if not os.path.isabs(root):
                root = os.path.join(cfg.get_root(), root)

        new_curr = set()

        # Recorrem tots els subdirectoris
        for dirpath, _, filenames in os.walk(root):
            for fname in filenames:
                if fname.lower().endswith(".png"):
                    abs_path = os.path.join(dirpath, fname)
                    # Path relatiu canònic a ROOT_DIR
                    rel_canon = cfg.get_canonical_pathfile(abs_path)
                    new_curr.add(rel_canon)

        self._added = sorted(list(new_curr - self._prev))
        self._removed = sorted(list(self._prev - new_curr))
        self._prev = new_curr

    """ 

    def reload_fs(self, path: str = None) -> None:
        # Determinar raíz
        if path is None:
            root = cfg.get_root()
        else:
            root = path
            if not os.path.isabs(root):
                root = os.path.join(cfg.get_root(), root)

        new_curr = set()
        # Recorrer filesystem y coleccionar rutas canónicas relativas a ROOT
        for raiz, _, archivos in os.walk(root):
            for archivo in archivos:
                if archivo.lower().endswith(".png"):
                    full_path = os.path.join(raiz, archivo)
                    rel_canon = cfg.get_canonical_pathfile(full_path)
                    new_curr.add(rel_canon)

        # detectar añadidos/eliminados y actualizar estado
        self._added = sorted(list(new_curr - self._prev))
        self._removed = sorted(list(self._prev - new_curr))
        self._prev = new_curr

    def files_added(self) -> list:
        return list(self._added)

    def files_removed(self) -> list:
        return list(self._removed)

    def __str__(self):
        return f'ImageFiles: Added {self._added}, Removed: {self._removed}'
    
    def __len__(self):
        return len(self._prev)