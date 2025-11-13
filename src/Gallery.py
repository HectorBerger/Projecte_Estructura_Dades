# -*- coding: utf-8 -*-
import cfg
import json
import os
from collections import deque
from ImageViewer import ImageViewer
from ImageID import ImageID
import glob
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

class Gallery():
    def __init__(self, image_viewer: ImageViewer = None, image_id: ImageID = None):
        if image_viewer is None and not (isinstance(image_viewer, ImageViewer)):
            raise TypeError("image_viewer ha de ser una instància d'ImageViewer o compatible")

        if image_id is None and not (isinstance(image_id, ImageID)):
            raise TypeError("image_id ha de ser una instància d'ImageID o compatible")


        self._uuids = deque()
        self._gallery_name = None
        self._gallery_description = None
        self._created_date = None
        self._image_viewer = image_viewer
        self._image_id = image_id
        self._file = None
    
    def __iter__(self):
        return iter(list(self._uuids))

    def _is_JsonFile(self, file:str) -> bool:  
        return file.lower().endswith('.json')

    def _is_JsonFile(self, file:str) -> bool:
        return file.lower().endswith('.json')

    def load_file(self, file: str) -> None:
        # Neteja la galeria anterior
        self._uuids.clear()
        if self._is_JsonFile(file) == False:
            return None

        root = cfg.get_root()
        abs_path = file if os.path.isabs(file) else os.path.join(root, file)
        abs_path = os.path.normpath(abs_path)

        if os.path.isdir(abs_path):
            json_files = glob(os.path.join(abs_path, "*.json"))
            if not json_files:
                raise FileNotFoundError(f"No s'ha trobat cap arxiu JSON dins del directori: {abs_path}")
            abs_path = json_files[0]
            abs_path = cfg.get_canonical_pathfile(abs_path)


        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"No s'ha trobat l'arxiu JSON: {abs_path}")

        self._file = cfg.get_canonical_pathfile(abs_path)

        with open(abs_path, 'r', encoding='utf-8') as f:    
            data = json.load(f)

        self._gallery_name = data.get('gallery_name', '')
        self._gallery_description = data.get('description', '')
        self._created_date = data.get('created_date', '')
        images = data.get('images', [])

        for rel_path in images:
            img_path = rel_path
            if not os.path.isabs(img_path):
                img_path = os.path.join(root, rel_path)
                canon = cfg.get_canonical_pathfile(img_path)
                # UUID coherent amb la resta del sistema
                if self._image_id is not None:
                    uuid = self._image_id.generate_uuid(img_path)
                else:
                    uuid = str(cfg.get_uuid(canon))
                if uuid is not None:
                    self._uuids.append(uuid)
                    print("DEBUG: Afegida imatge a la galeria:", img_path, "UUID:", uuid) #NUNCA LLEGA AQUí

    def show(self) -> None:
        # Galeria buida o sense viewer → res a fer
        if not self._uuids or self._image_viewer is None:
            return

        for uuid in list(self._uuids):
            self._image_viewer.show_image(uuid, 2)
    
    def add_image_at_end(self, uuid: str) -> None:
        self._uuids.append(uuid)

    def remove_first_image(self) -> None:
        # Deixem que deque llanci IndexError si està buida (el test ho comprova)
        if len(self._uuids) == 0:
            return None
        self._uuids.popleft()
        
    def remove_last_image(self) -> None:
        if len(self._uuids) == 0:
            return None
        self._uuids.pop()

    def __str__(self):
        return 'Gallery: ' + ', '.join(self._uuids)
    
    def __len__(self):
        return len(self._uuids)