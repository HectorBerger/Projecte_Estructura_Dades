# -*- coding: utf-8 -*-
import cfg
import json
import os
import copy
from collections import deque
from ImageViewer import ImageViewer
import time
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
    def __init__ (self, llista=None, Image_viewer : ImageViewer= None):
        self._fitxer = None
        self._uuids = deque()
        self._gallery_name = None
        self._gallery_description = None
        self._created_date = None
        self._Image_viewer = Image_viewer
        if isinstance(llista, list):
            self.crear_desde_llista(llista)

    def load_file(self, file:str = ''):
        self._file = file
        try:
            with open(file, 'r') as file:
                json_string = json.load(file)
                self._gallery_name = json_string['gallery_name']
                self._gallery_description = json_string['description']
                self._created_date = json_string['created_date']
                list_file_paths = json_string['images']
        except FileNotFoundError as e:
            raise (f'Fixter no trobat {e}')
        root_path = cfg.get_root()
        for file_path in list_file_paths:
            file_path = os.path.join(root_path, file_path)
            if os.path.exists(file_path):
                self._uuids.append(cfg.get_uuid(file_path))

    def crear_desde_llista(self,llista: list = None):
        for uuid in llista:
            self.add_image_at_end(uuid)
        self._gallery_description = f'Galeria Customizada'
        self._gallery_name = f'Galeria generada desda una cerca de coincidencia en algu parametre de la metadata de les imatges'
        self._created_date = time.time()

    def show(self, mode):
        for uuid in self._uuids:
            self._Image_viewer.show_image(uuid, mode)
    
    def add_image_at_end(self, uuid:str = ''):
        self._uuids.append(uuid)

    def remove_first_image(self):
        hola = self._uuids.popleft()
        
    def remove_last_image(self):
        hola = self._uudis.pop()




