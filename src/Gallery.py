# -*- coding: utf-8 -*-
import cfg
import json
import os
import copy
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

def Gallery():
    def __init__ (self, fitxer: str=''):
        self._fitxer = fitxer
        self._relative_paths = dict()
        self._gallery_name = None
        self._gallery_description = None
        self._created_date = None
        try:
            with open(fitxer, 'r') as file:
                json_string = json.load(file)
                self._gallery_name = json_string['gallery_name']
                self._gallery_description = json_string['description']
                self._created_date = json_string['created_date']
                list_file_paths = json_string['images']
        except FileNotFoundError as e:
            raise (f'Fixter no trobat {e}')
        root_path = cfg.get_root()
        for file_path in list_file_paths:
            relative_path = copy.deepcopy(file_path)
            file_path = os.path.join(root_path, file_path)
            if os.path.exists(file_path):
                self._hashmap[cfg.get_uuid(file_path)] = relative_path





