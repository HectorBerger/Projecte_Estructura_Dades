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
        # Guarda l'estat anterior dels arxius PNG trobats
        self._prev = set()
        # Guarda la llista d'arxius afegits des de l'última lectura
        self._added = []
        # Guarda la llista d'arxius eliminats des de l'última lectura
        self._removed = []

    def reload_fs(self, path: str = None) -> None:
        # Obté el directori arrel des de la configuració
        if path is None:
            root = cfg.get_root()
        else:
            root = path
        new_curr = set()

        # Recorre tots els subdirectoris i fitxers
        for dirpath, _, filenames in os.walk(root): #aqui la _ es para no mirar las subcarpetas, pero no tengo claro si hay q mirarlas o no, es a lo duda
            for fname in filenames:
                # Només considera arxius amb extensió .png (no sensible a majúscules)
                if fname.lower().endswith(".png"):
                    abs_path = os.path.join(dirpath, fname)
                    # Obté el path relatiu i canònic respecte a ROOT_DIR
                    rel_canon = cfg.get_canonical_pathfile(abs_path)
                    new_curr.add(rel_canon)

        # Calcula els arxius afegits (estan a new_curr però no a _prev)
        self._added = sorted(list(new_curr - self._prev))
        # Calcula els arxius eliminats (estan a _prev però no a new_curr)
        self._removed = sorted(list(self._prev - new_curr))
        # Actualitza l'estat anterior per a la següent crida
        self._prev = new_curr

    def files_added(self) -> list:
        # Retorna la llista d'arxius afegits des de l'última crida a reload_fs
        return list(self._added)

    def files_removed(self) -> list:
        # Retorna la llista d'arxius eliminats des de l'última crida a reload_fs
        return list(self._removed)

    def __str__(self):
        return 'hola'
    
    def __len__(self):
        return 0