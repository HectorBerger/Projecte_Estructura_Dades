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
        # Estat de l'escaneig anterior (set de paths relatius canònics)
        self._prev: set[str] = set()
        # Deltas entre l'últim reload i l'actual
        self._added: list[str] = []
        self._removed: list[str] = []

    def reload_fs(self, path: str) -> None:
        # Si ens passen una cadena buida o None, fem servir la config
        root = path if path else cfg.get_root()

        if not os.path.isdir(root):
            # Si el path no existeix, no toquem l'estat anterior però netegem deltes
            print(f"[ImageFiles] Avís: el directori no existeix: {root}")
            self._added = []
            self._removed = []
            return

        new_curr: set[str] = set()

        # os.walk recorre recursivament subdirectoris.
        # El segon valor (dirnames) no l'usem explícitament, però la recursió hi és.
        for dirpath, _dirnames, filenames in os.walk(root):
            for fname in filenames:
                if fname.lower().endswith(".png"):
                    abs_path = os.path.join(dirpath, fname)
                    # Canonitza a RELATIU respecte ROOT_DIR
                    rel_canon = cfg.get_canonical_pathfile(abs_path)
                    new_curr.add(rel_canon)

        added = new_curr - self._prev
        removed = self._prev - new_curr

        # Desa versions ordenades i IMMUTABLES cap enfora
        self._added = sorted(added)
        self._removed = sorted(removed)

        # Actualitza l'estat per la propera vegada
        self._prev = new_curr

    def files_added(self) -> list:
        """Retorna els paths relatius dels arxius nous des de l'últim reload."""
        return list(self._added)

    def files_removed(self) -> list:
        """Retorna els paths relatius dels arxius que han desaparegut des de l'últim reload."""
        return list(self._removed)